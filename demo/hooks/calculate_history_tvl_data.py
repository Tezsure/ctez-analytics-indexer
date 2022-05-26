
from tracemalloc import start
from dipdup.context import HookContext
from datetime import datetime, timedelta
import demo.models as models
from demo.functions.Tvl_stats.calculate_history_tvl import history_tvl
from demo.functions.Tvl_stats.calculate_history_pool import history_pool
from demo.functions.Tvl_stats.dollar import dollar_stats
from decimal import Decimal;
from demo.functions.Tvl_stats.calculate_pool_history import pool_history
from demo.functions.Tvl_stats.calculate_tvl_history import tvl_history
from demo.functions.Tvl_stats.history_dollar import history_dollar_stats
from demo.functions.Weekly.Tvl_stats.calculate_history_weekly_tvl import history_tvl_weekly
from dateutil.relativedelta import *


async def calculate_history_tvl_data(
    ctx: HookContext,
    major: bool,
) -> None:
    start_date = datetime(2022, 2, 1);
    start_date_weekly = datetime(2022, 2, 1);
    start_date_monthly = datetime(2022, 2, 1);
    iteration = timedelta(hours=24);
    iteration_month = relativedelta(months=+1)
    end_date = datetime.utcnow();

    # ctx.logger.info("Hey %s", start_date + iteration_month);
    # ctx.logger.info("Hey %s", start_date + iteration);
    while start_date<=end_date:
        data = await history_tvl(start_date);
        data1 = await history_pool(start_date);
        dollars = await dollar_stats(start_date);
        
        if data==0:
            data = await tvl_history();
        
        if data1==0:
            data1 = await pool_history();

        if dollars==0:
            dollars = await history_dollar_stats();
        # ctx.logger.info("Hey %s", data);
        amount = Decimal((Decimal(data) + Decimal(data1))*Decimal(dollars));
        # amount = str(amount);
        tvl_store = await models.Tvl_data.create(
        tvl = round(amount, 5),
        timestamp = start_date
        )
        start_date+=iteration;

    # Monthly Data

    while start_date_monthly<=end_date:
        month_ago_time = start_date_monthly - iteration_month;
        tvl_data = await history_tvl_weekly(start_date_monthly, month_ago_time);
        # print(tvl_data);
        tvl_store = await models.Tvl_data_Monthly.create(
            tvl = round(tvl_data, 5),
            timestamp_from = month_ago_time,
            timestamp_to = start_date_monthly
        ) 
        start_date_monthly+=iteration_month
    
    if start_date_monthly!=end_date:
        start_date_monthly -= iteration_month;
        tvl_data = await history_tvl_weekly(end_date, start_date_monthly);
        tvl_store = await models.Tvl_data_Monthly.create(
            tvl = round(tvl_data, 5),
            timestamp_from = start_date_monthly,
            timestamp_to = end_date
        ) 

    ctx.logger.info("Hey Man, how are you")