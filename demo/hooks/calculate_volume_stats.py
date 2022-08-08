from dipdup.context import HookContext
import demo.models as models
from datetime import datetime, timedelta
from demo.functions.Price_stats.block_level import get_level
from demo.functions.Volume_stats.calculate_buy_volume_ctez import buy_volume_of_24hours
from demo.functions.Volume_stats.calculate_sell_volume_ctez import sell_volume_of_24hours
from demo.functions.Volume_stats.buy_sell_volume import buy_sell_volume_percentage
from demo.functions.Volume_stats.ctez_volume_days import volume_days
from demo.functions.Weekly.Volume_stats.calculate_history_volume_monthly import history_volume_monthly
from dateutil.relativedelta import *
import pytz
from demo.functions.Tvl_stats.history_dollar import history_dollar_stats

async def calculate_volume_stats(
    ctx: HookContext,
    major: bool,
) -> None:
    
    timestamp_now = datetime.utcnow();
    level = await get_level();
    
    # Volume Calculation for ctez for 24 hours
    dollars = await history_dollar_stats();
    buy_volume_24hours_ctez = await buy_volume_of_24hours();
    sell_volume_24hours_ctez = await sell_volume_of_24hours();
    volume_24hours_ctez = buy_volume_24hours_ctez + sell_volume_24hours_ctez;
    volume_24hours_ctez = float(float(volume_24hours_ctez)*float(dollars));
    
    buy_volume_percentage = await buy_sell_volume_percentage(buy_volume_24hours_ctez, volume_24hours_ctez);
    sell_volume_percentage = await buy_sell_volume_percentage(sell_volume_24hours_ctez, volume_24hours_ctez);
    
    volume_7days_ctez = await volume_days(7);
    volume_1month_ctez = await volume_days(30);
    
    volume_stats = models.volumestats(
        token_symbol = 'ctez',
        volume_24hours = round(volume_24hours_ctez, 5),
        buy_volume = round(buy_volume_24hours_ctez, 5),
        sell_volume = round(sell_volume_24hours_ctez, 5),
        buy_volume_percentage_24hours = round(buy_volume_percentage, 5),
        sell_volume_percentage_24hours = round(sell_volume_percentage, 5),
        volume_7days = round(volume_7days_ctez, 5),
        volume_1month = round(volume_1month_ctez, 5),
        level = level,
        timestamp = timestamp_now,
        epoch_timestamp = int(timestamp_now.timestamp()*1000)
    )
    
    await volume_stats.save();


    # Month
    volume_values_month = await models.volumestats_monthly\
                       .all()\
                       .order_by("-timestamp_from")\
                       .first();
    iteration_month = relativedelta(months=+1)
    start_date_monthly = volume_values_month.timestamp_from;
    end_date_monthly = volume_values_month.timestamp_to;
    total_month = start_date_monthly + iteration_month
    timestamp_now = pytz.utc.localize(timestamp_now);
    if timestamp_now - total_month <=timedelta(hours=0):
        volume_data = await history_volume_monthly(timestamp_now, start_date_monthly);
        tvl_table = await models.volumestats_monthly.update_or_create(
            id = volume_values_month.id,
            defaults={
                'token_symbol': 'ctez',
                'volume': round(volume_data, 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : timestamp_now,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' : int(timestamp_now.timestamp()*1000)
            }
        );
    else:
        volume_data_prev = await history_volume_monthly(total_month, start_date_monthly);
        tvl_table_prev = await models.volumestats_monthly.update_or_create(
            id = volume_values_month.id,
            defaults={
                'token_symbol': 'ctez',
                'volume': round(volume_data_prev, 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : total_month,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' : int(total_month.timestamp()*1000)
            }
        );


        volume_data = await history_volume_monthly(timestamp_now, total_month);
        tvl_table = await models.volumestats_monthly.create(
            token_symbol = 'ctez',
            volume = round(volume_data, 6),
            timestamp_from = total_month,
            timestamp_to = timestamp_now,
            epoch_timestamp_from = int(total_month.timestamp()*1000),
            epoch_timestamp_to = int(timestamp_now.timestamp()*1000)
        );



    
    
    