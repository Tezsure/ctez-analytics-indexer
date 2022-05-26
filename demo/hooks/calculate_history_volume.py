
from sqlite3 import Timestamp
from dipdup.context import HookContext
from decimal import Decimal
import demo.models as models
from datetime import datetime, timedelta
from demo.functions.Volume_stats.history_of_volume import history_volume_days
from demo.functions.Volume_stats.calculate_buy_volume_ctez import buy_volume_of_24hours
from demo.functions.Volume_stats.calculate_sell_volume_ctez import sell_volume_of_24hours
from demo.functions.Volume_stats.buy_sell_volume import buy_sell_volume_percentage
from demo.functions.Volume_stats.calculate_history_buy_volume import buy_volume_of_24hours_history
from demo.functions.Volume_stats.calculate_history_sell_volume import sell_volume_of_24hours_history
from demo.functions.Price_stats.history_block_level import get_history_level
from dateutil.relativedelta import *
from demo.functions.Weekly.Volume_stats.calculate_history_volume_monthly import history_volume_monthly


async def calculate_history_volume(
    ctx: HookContext,
    major: bool,
) -> None:
    end_date = datetime.utcnow();
    start_date = datetime(2022, 2, 1);
    iteration = timedelta(hours=24);
    iteration_month = relativedelta(months=+1)
    start_date_monthly = datetime(2022, 2, 1);
    
    while start_date <= end_date:
        history_volume_24hours = await history_volume_days(start_date, 1);
        history_volume_7days = await history_volume_days(start_date, 7);
        history_volume_1month = await history_volume_days(start_date, 30);
        buy_volume_24hours_ctez = await buy_volume_of_24hours_history(start_date);
        sell_volume_24hours_ctez = await sell_volume_of_24hours_history(start_date);
        level = await get_history_level(start_date);

        if buy_volume_24hours_ctez == 0:
            buy_volume_24hours_ctez = await buy_volume_of_24hours();

        if sell_volume_24hours_ctez == 0:
            sell_volume_24hours_ctez = await sell_volume_of_24hours();

        buy_volume_percentage = await buy_sell_volume_percentage(buy_volume_24hours_ctez, history_volume_24hours);
        sell_volume_percentage = await buy_sell_volume_percentage(sell_volume_24hours_ctez, history_volume_24hours);
        volume_stats = models.volumestats(
            token_symbol = 'ctez',
            volume_24hours = round(history_volume_24hours, 5),
            buy_volume = round(buy_volume_24hours_ctez, 5),
            sell_volume = round(sell_volume_24hours_ctez, 5),
            buy_volume_percentage_24hours = round(buy_volume_percentage, 5),
            sell_volume_percentage_24hours = round(sell_volume_percentage, 5),
            volume_7days = round(history_volume_7days, 5),
            volume_1month = round(history_volume_1month, 5),
            level = level,
            timestamp = start_date
        )
        await volume_stats.save();
        
        start_date+=iteration;
    
    # Monthly Data

    while start_date_monthly<=end_date:
        month_ago_time = start_date_monthly - iteration_month;
        volume_data = await history_volume_monthly(start_date_monthly, month_ago_time);
        tvl_store = await models.volumestats_monthly.create(
            token_symbol = 'ctez',
            volume = round(volume_data, 5),
            timestamp_from = month_ago_time,
            timestamp_to = start_date_monthly
        ) 
        start_date_monthly+=iteration_month
    
    if start_date_monthly!=end_date:
        start_date_monthly -= iteration_month;
        volume_data = await history_volume_monthly(end_date, start_date_monthly);
        tvl_store = await models.volumestats_monthly.create(
            token_symbol = 'ctez',
            volume = round(volume_data, 5),
            timestamp_from = start_date_monthly,
            timestamp_to = end_date
        ) 
    ctx.logger.info("Hey Man, how are you")
    if(start_date>=end_date):
        return;