
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
    tez_price_stats = float(1/ctez_price_stats);
    price_change_percentage_24hour = await price_change_stats(ctez_price_stats, 1);
    price_change_percentage_7days = await price_change_stats(ctez_price_stats, 7);
    price_change_percentage_1month = await price_change_stats(ctez_price_stats, 30);
    price_change_percentage_1year = await price_change_stats(ctez_price_stats, 365);
    stats = await models.pricestats(
        token_symbol = 'ctez',
        ctez_price = round(ctez_price_stats, 5),
        tez_price = tez_price_stats,
        price_change_24hours = round(price_change_percentage_24hour, 5),
        price_change_7days = round(price_change_percentage_7days, 5),
        prce_change_1month = round(price_change_percentage_1month, 5),
        price_change_1year = round(price_change_percentage_1year, 5),
        level = level,
        timestamp = end_date
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
        # print("Hey babe", price_values_month.id);
        price_table = await models.pricestats_monthly.update_or_create(
            id = price_values_month.id,
            defaults={
                'token_symbol' : 'ctez',
                'ctez_price': round(price_data['current_avg_ctez_price'], 5),
                'tez_price': round(price_data['current_avg_tez_target'], 5),
                'timestamp_from': start_date_monthly,
                'timestamp_to' : end_date
            }
        );
    else:
        price_data = await history_price_weekly_monthly(end_date, total_month);
        price_table = await models.pricestats_monthly.create(
            token_symbol = 'ctez',
            ctez_price = round(price_data['current_avg_ctez_price'], 5),
            tez_price = round(price_data['current_avg_tez_target'], 5),
            timestamp_from = total_month,
            timestamp_to = end_date
        );
