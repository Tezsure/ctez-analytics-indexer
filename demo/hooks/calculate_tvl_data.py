
from decimal import Decimal
from time import time
from demo.functions.Tvl_stats.dollar import dollar_stats
from dipdup.context import HookContext
import demo.models as models
from demo.functions.Tvl_stats.calculate_tvl import tvl_stats
from datetime import datetime, timedelta
from decimal import Decimal
from demo.functions.Tvl_stats.history_dollar import history_dollar_stats;
from demo.functions.Tvl_stats.calculate_tvl_history import tvl_history
from demo.functions.Tvl_stats.calculate_pool_history import pool_history
from demo.functions.Tvl_stats.calculate_ctez_pool_history import ctez_pool_history
from dateutil.relativedelta import *
import pytz
from demo.functions.Weekly.Tvl_stats.calculate_history_weekly_tvl import history_tvl_weekly
from demo.functions.Main_stats.main_history import main_history_data

async def calculate_tvl_data(
    ctx: HookContext,
    major: bool,
) -> None:
    tez_dollar = await history_dollar_stats();
    tvl_data = await tvl_history();
    data = await pool_history();
    ctez_data = await ctez_pool_history();
    start = datetime.utcnow();
    start = pytz.utc.localize(start);
    main_data = await main_history_data();
    
    if not tez_dollar:
        return;
    oven_tvl_data = float(tvl_data * tez_dollar)
    amm_tvl_data = float(float(ctez_data)*float(main_data.current_price) + float(data))*float(tez_dollar)
    tvl_store = await models.Tvl_data.create(
        oven_tvl = round(oven_tvl_data, 6),
        amm_tvl = round(amm_tvl_data, 6),
        timestamp = start,
        epoch_timestamp = int(start.timestamp()*1000)
    )

    # Month
    tvl_values_month = await models.Tvl_data_Monthly\
                       .all()\
                       .order_by("-timestamp_from")\
                       .first();
    iteration_month = relativedelta(months=+1)
    start_date_monthly = tvl_values_month.timestamp_from;
    end_date_monthly = tvl_values_month.timestamp_to;
    total_month = start_date_monthly + iteration_month
    if start - total_month <=timedelta(hours=0):
        tvl_data = await history_tvl_weekly(start, start_date_monthly);
        tvl_table = await models.Tvl_data_Monthly.update_or_create(
            id = tvl_values_month.id,
            defaults={
                'oven_tvl': round(tvl_data['avg_tvl_data'], 6),
                'amm_tvl' : round(tvl_data['avg_amm_tvl_data'], 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : start,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' : int(start.timestamp()*1000)
            }
        );
    else:
        tvl_data_prev = await history_tvl_weekly(total_month, start_date_monthly);
        tvl_table = await models.Tvl_data_Monthly.update_or_create(
            id = tvl_values_month.id,
            defaults={
                'oven_tvl': round(tvl_data_prev['avg_tvl_data'], 6),
                'amm_tvl' : round(tvl_data_prev['avg_amm_tvl_data'], 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : total_month,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' : int(total_month.timestamp()*1000)
            }
        );
    
        tvl_data = await history_tvl_weekly(start, total_month);
        tvl_table = await models.Tvl_data_Monthly.create(
            oven_tvl = round(tvl_data['avg_tvl_data'], 6),
            amm_tvl = round(tvl_data['avg_amm_tvl_data'], 6),
            timestamp_from = total_month,
            timestamp_to = start,
            epoch_timestamp_from = int(total_month.timestamp()*1000),
            epoch_timestamp_to = int(start.timestamp()*1000)
        );



    