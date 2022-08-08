
from tracemalloc import start
from dipdup.context import HookContext
from datetime import datetime, timedelta
import demo.models as models
from demo.functions.Price_stats.history_of_price import history_price
from decimal import Decimal
from demo.functions.Price_stats.change_price import price_change_stats
from demo.functions.Price_stats.price_stats import price_stats_provider
from demo.functions.Price_stats.change_price_history import price_change_stats_history
from demo.functions.Price_stats.history_block_level import get_history_level
from dateutil.relativedelta import *
from demo.functions.Weekly.Price_stats.calculate_history_weekly_monthly_price import history_price_weekly_monthly

async def calculate_history_price(
    ctx: HookContext,
    major: bool,
) -> None:
    
    end_date = datetime.utcnow();
    start_date = datetime(2022, 2, 1);
    start_date_weekly = datetime(2022, 2, 1);
    start_date_monthly = datetime(2022, 2, 1);
    iteration = timedelta(hours=24);
    iteration_week = timedelta(days=7);
    iteration_month = relativedelta(months=+1)
    
    while start_date <= end_date:
        ctez_price_stats = await history_price(start_date)
        level = await get_history_level(start_date);

        if ctez_price_stats == 0:
            ctez_price_stats = await price_stats_provider();

        tez_price_stats = float(1/ctez_price_stats);

        price_change_percentage_24hour = await price_change_stats_history(ctez_price_stats, start_date, 1);

        if price_change_percentage_24hour == 0:
            price_change_percentage_24hour = await price_change_stats(ctez_price_stats, 1);


        price_change_percentage_7days = await price_change_stats_history(ctez_price_stats, start_date, 7);
        price_change_percentage_1month = await price_change_stats_history(ctez_price_stats, start_date, 30);
        price_change_percentage_1year = await price_change_stats_history(ctez_price_stats, start_date, 365);
        
        stats = await models.pricestats(
            token_symbol = 'ctez',
            ctez_price = ctez_price_stats,
            tez_price = tez_price_stats,
            price_change_24hours = round(float(price_change_percentage_24hour), 6),
            price_change_7days = round(float(price_change_percentage_7days), 6),
            prce_change_1month = round(float(price_change_percentage_1month), 6),
            price_change_1year = round(float(price_change_percentage_1year), 6),
            level = level,
            timestamp = start_date,
            epoch_timestamp = int(start_date.timestamp()*1000)
        )
        await stats.save();
        
        start_date+=iteration;
    
    # Monthly Data

    while start_date_monthly<=end_date:
        month_ago_time = start_date_monthly - iteration_month;
        price_data = await history_price_weekly_monthly(start_date_monthly, month_ago_time);
        price_store = await models.pricestats_monthly.create(
            token_symbol = 'ctez',
            ctez_price = round(price_data['current_avg_ctez_price'], 6),
            timestamp_from = month_ago_time,
            timestamp_to = start_date_monthly,
            epoch_timestamp_from = int(month_ago_time.timestamp()*1000),
            epoch_timestamp_to = int(start_date_monthly.timestamp()*1000)
        ) 
        start_date_monthly+=iteration_month
    
    if start_date_monthly!=end_date:
        start_date_monthly -= iteration_month;
        price_data = await history_price_weekly_monthly(end_date, start_date_monthly);
        price_store = await models.pricestats_monthly.create(
            token_symbol = 'ctez',
            ctez_price = round(price_data['current_avg_ctez_price'], 6),
            timestamp_from = start_date_monthly,
            timestamp_to = end_date,
            epoch_timestamp_from = int(start_date_monthly.timestamp()*1000),
            epoch_timestamp_to = int(end_date.timestamp()*1000)
        ) 

    if(start_date>=end_date):
        return;