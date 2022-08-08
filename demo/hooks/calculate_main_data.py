
from dipdup.context import HookContext
import demo.models as models
from datetime import datetime
from decimal import Decimal
from demo.functions.Main_stats.main_history import main_history_data
from dateutil.relativedelta import *
import pytz
from demo.functions.Weekly.Main_data_stats.calculate_history_weekly_monthly_maindata import history_main_data_weekly_monthly
from datetime import datetime, timedelta

async def calculate_main_data(
    ctx: HookContext,
    major: bool,
) -> None:
    start_time = datetime.utcnow();
    data = await main_history_data();
    
    mainpage =  await models.MainDataRegularize.create(
        current_target = round(data.current_target, 5),
        current_price = round(data.current_price, 5),
        premium = round(data.premium, 5),
        current_annual_drift = data.current_annual_drift, 
        timestamp = start_time,
        epoch_timestamp = int(start_time.timestamp()*1000)
    )

    # Month
    tvl_values_month = await models.MainDataRegularize_monthly\
                       .all()\
                       .order_by("-timestamp_from")\
                       .first();
    iteration_month = relativedelta(months=+1)
    start_date_monthly = tvl_values_month.timestamp_from;
    end_date_monthly = tvl_values_month.timestamp_to;
    total_month = start_date_monthly + iteration_month
    start_time = pytz.utc.localize(start_time);
    if start_time - total_month <=timedelta(hours=0):
        main_data = await history_main_data_weekly_monthly(start_time, start_date_monthly);
        main_table = await models.MainDataRegularize_monthly.update_or_create(
            id = tvl_values_month.id,
            defaults={
                'current_price': round(main_data['current_avg_price'], 6),
                'current_target': round(main_data['current_avg_target'], 6),
                'premium': round(main_data['current_avg_premium'], 6),
                'current_annual_drift': round(main_data['current_avg_annual_drift'], 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : start_time,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' : int(start_time.timestamp()*1000)
            }
        );
    else:
        main_data_prev = await history_main_data_weekly_monthly(total_month, start_date_monthly);
        main_table_prev = await models.MainDataRegularize_monthly.update_or_create(
            id = tvl_values_month.id,
            defaults={
                'current_price': round(main_data_prev['current_avg_price'], 6),
                'current_target': round(main_data_prev['current_avg_target'], 6),
                'premium': round(main_data_prev['current_avg_premium'], 6),
                'current_annual_drift': round(main_data_prev['current_avg_annual_drift'], 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : total_month,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' : int(total_month.timestamp()*1000)
            }
        );

        main_data = await history_main_data_weekly_monthly(start_time, total_month);
        main_table = await models.MainDataRegularize_monthly.create(
            current_price = round(main_data['current_avg_price'], 6),
            current_target = round(main_data['current_avg_target'], 6),
            premium = round(main_data['current_avg_premium'], 6),
            current_annual_drift = round(main_data['current_avg_annual_drift'], 6),
            timestamp_from = total_month,
            timestamp_to = start_time,
            epoch_timestamp_from = int(total_month.timestamp()*1000),
            epoch_timestamp_to = int(start_time.timestamp()*1000)
        );