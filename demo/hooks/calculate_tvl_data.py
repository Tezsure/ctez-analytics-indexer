
from decimal import Decimal
from time import time
from dipdup.context import HookContext
import demo.models as models
from demo.functions.Tvl_stats.calculate_tvl import tvl_stats
from datetime import datetime, timedelta
from decimal import Decimal
from demo.functions.Tvl_stats.history_dollar import history_dollar_stats;
from demo.functions.Tvl_stats.calculate_tvl_history import tvl_history
from demo.functions.Tvl_stats.calculate_pool_history import pool_history
from dateutil.relativedelta import *
import pytz
from demo.functions.Weekly.Tvl_stats.calculate_history_weekly_tvl import history_tvl_weekly

async def calculate_tvl_data(
    ctx: HookContext,
    major: bool,
) -> None:
    # tvl_data = await tvl_stats();
    # tez_dollar = await models.Token_USD\
    #             .all()      
    tez_dollar = await history_dollar_stats();
    tvl_data = await tvl_history();
    data = await pool_history();
    start = datetime.utcnow();
    start = pytz.utc.localize(start);
    
    if not tez_dollar:
        return;
    # ctx.logger.info("Hey babe %s", tez_dollar[1].price);
    # data = await ctx.get_tzkt_datasource('tzkt_mainnet').get_contract_storage('KT1H5b7LxEExkFd2Tng77TfuWbM5aPvHstPr');
    # ctx.logger.info("Hey %s", tvl_data);
    amount = float((Decimal(tvl_data) + 2*Decimal(data)/(10 ** 6))*Decimal(tez_dollar))
    # amount = str(amount);
    # ctx.logger.info("HEy man %s", str(amount));
    tvl_store = await models.Tvl_data.create(
        tvl = round(amount, 5),
        timestamp = start
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
        print("Hey babe", tvl_values_month.id);
        tvl_table = await models.Tvl_data_Monthly.update_or_create(
            id = tvl_values_month.id,
            defaults={
                'tvl': round(tvl_data, 5),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : start
            }
        );
    else:
        tvl_data = await history_tvl_weekly(start, total_month);
        tvl_table = await models.Tvl_data_Monthly.create(
            tvl = round(tvl_data, 5),
            timestamp_from = total_month,
            timestamp_to = start
        );



    