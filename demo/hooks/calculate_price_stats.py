
from dipdup.context import HookContext
from datetime import datetime, timedelta
import demo.models as models
from decimal import Decimal
from demo.functions.Price_stats.price_stats import price_stats_provider
from demo.functions.Price_stats.change_price import price_change_stats
from demo.functions.Price_stats.block_level import get_level
from dateutil.relativedelta import *
import pytz
from demo.functions.Weekly.Price_stats.calculate_history_weekly_monthly_price import history_price_weekly_monthly

async def calculate_price_stats(
    ctx: HookContext,
    major: bool,
) -> None:
    
    
    end_date = datetime.utcnow();
    level = await get_level();
    ctez_price_stats = await price_stats_provider()
    price_change_percentage_24hour = await price_change_stats(ctez_price_stats, 1);
    price_change_percentage_7days = await price_change_stats(ctez_price_stats, 7);
    price_change_percentage_1month = await price_change_stats(ctez_price_stats, 30);
    price_change_percentage_1year = await price_change_stats(ctez_price_stats, 365);
    stats = await models.pricestats(
        token_symbol = 'ctez',
        ctez_price = round(ctez_price_stats, 6),
        price_change_24hours = round(price_change_percentage_24hour, 6),
        price_change_7days = round(price_change_percentage_7days, 6),
        prce_change_1month = round(price_change_percentage_1month, 6),
        price_change_1year = round(price_change_percentage_1year, 6),
        level = level,
        timestamp = end_date,
        epoch_timestamp = int(end_date.timestamp()*1000)
    )
    await stats.save();

    # Month

    price_values_month = await models.pricestats_monthly\
                       .all()\
                       .order_by("-timestamp_from")\
                       .first();
    iteration_month = relativedelta(months=+1)
    start_date_monthly = price_values_month.timestamp_from;
    end_date_monthly = price_values_month.timestamp_to;
    total_month = start_date_monthly + iteration_month
    end_date = pytz.utc.localize(end_date);
    if end_date - total_month <=timedelta(hours=0):
        price_data = await history_price_weekly_monthly(end_date, start_date_monthly);
        price_table = await models.pricestats_monthly.update_or_create(
            id = price_values_month.id,
            defaults={
                'token_symbol' : 'ctez',
                'ctez_price': round(price_data['current_avg_ctez_price'], 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : end_date,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' :  int(end_date.timestamp()*1000)
            }
        );
    else:
        price_data_prev = await history_price_weekly_monthly(total_month, start_date_monthly);
        price_table_prev = await models.pricestats_monthly.update_or_create(
            id = price_values_month.id,
            defaults={
                'token_symbol' : 'ctez',
                'ctez_price': round(price_data_prev['current_avg_ctez_price'], 6),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : total_month,
                'epoch_timestamp_from' : int(start_date_monthly.timestamp()*1000),
                'epoch_timestamp_to' :  int(total_month.timestamp()*1000)
            }
        );

        
        price_data = await history_price_weekly_monthly(end_date, total_month);
        price_table = await models.pricestats_monthly.create(
            token_symbol = 'ctez',
            ctez_price = round(price_data['current_avg_ctez_price'], 6),
            timestamp_from = total_month,
            timestamp_to = end_date,
            epoch_timestamp_from = int(total_month.timestamp()*1000),
            epoch_timestamp_to = int(end_date.timestamp()*1000)
        );
