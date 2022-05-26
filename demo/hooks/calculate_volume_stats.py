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

async def calculate_volume_stats(
    ctx: HookContext,
    major: bool,
) -> None:
    
    timestamp_now = datetime.utcnow();
    level = await get_level();
    
    # Volume Calculation for ctez for 24 hours
    
    buy_volume_24hours_ctez = await buy_volume_of_24hours();
    sell_volume_24hours_ctez = await sell_volume_of_24hours();
    volume_24hours_ctez = buy_volume_24hours_ctez + sell_volume_24hours_ctez;
    
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
        timestamp = timestamp_now
    )
    
    await volume_stats.save();


    # Month
    volume_values_month = await models.Tvl_data_Monthly\
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
        # print("Hey babe", volume_values_month.id);
        tvl_table = await models.volumestats_monthly.update_or_create(
            id = volume_values_month.id,
            defaults={
                'token_symbol': 'ctez',
                'volume': round(volume_data, 5),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : timestamp_now
            }
        );
    else:
        volume_data = await history_volume_monthly(timestamp_now, total_month);
        tvl_table = await models.volumestats_monthly.create(
            token_symbol = 'ctez',
            volume = round(volume_data, 5),
            timestamp_from = total_month,
            timestamp_to = timestamp_now
        );



    
    
    