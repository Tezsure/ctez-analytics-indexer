from tracemalloc import start
from dipdup.context import HookContext
from datetime import datetime, timedelta
import demo.models as models
from demo.functions.Tvl_stats.calculate_history_tvl import history_tvl
from demo.functions.Tvl_stats.calculate_history_pool import history_pool
from demo.functions.Tvl_stats.dollar import dollar_stats
from decimal import Decimal;
from demo.functions.Tvl_stats.calculate_pool_history import pool_history
from demo.functions.Tvl_stats.calculate_history_pool_ctez import history_pool_ctez
from demo.functions.Tvl_stats.calculate_ctez_pool_history import ctez_pool_history
from demo.functions.Tvl_stats.calculate_tvl_history import tvl_history
from demo.functions.Tvl_stats.history_dollar import history_dollar_stats
from demo.functions.Weekly.Tvl_stats.calculate_history_weekly_tvl import history_tvl_weekly
from dateutil.relativedelta import *
from demo.functions.Main_stats.history_main import history_main_data
from demo.functions.Main_stats.main_history import main_history_data

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
        ctez_data = await history_pool_ctez(start_date);
        main_data = await history_main_data(start_date);

        if main_data == 0:
            main_data = await main_history_data();

        if ctez_data == 0:
            ctez_data = await ctez_pool_history();
        
        if data==0:
            data = await tvl_history();
        
        if data1==0:
            data1 = await pool_history();

        if dollars==0:
            dollars = await history_dollar_stats();
        # ctx.logger.info("Hey %s", data);
        amount = Decimal((Decimal(data))*Decimal(dollars));
        # amm_amount = ;
        amm_amount = Decimal(Decimal(ctez_data*main_data.current_price + data1)*dollars);
        # amount = str(amount);
        tvl_store = await models.Tvl_data.create(
        oven_tvl = round(amount, 6),
        amm_tvl =  round(amm_amount, 6),
        timestamp = start_date,
        epoch_timestamp = int(start_date.timestamp()*1000)
        )
        start_date+=iteration;

    # Monthly Data

    while start_date_monthly<=end_date:
        month_ago_time = start_date_monthly - iteration_month;
        tvl_data = await history_tvl_weekly(start_date_monthly, month_ago_time);
        # print(tvl_data);
        tvl_store = await models.Tvl_data_Monthly.create(
            oven_tvl = round(tvl_data['avg_tvl_data'], 6),
            amm_tvl = round(tvl_data['avg_amm_tvl_data'], 6),
            timestamp_from = month_ago_time,
            timestamp_to = start_date_monthly,
            epoch_timestamp_from = int(month_ago_time.timestamp()*1000),
            epoch_timestamp_to = int(start_date_monthly.timestamp()*1000)
        ) 
        start_date_monthly+=iteration_month
    
    if start_date_monthly!=end_date:
        start_date_monthly -= iteration_month;
        tvl_data = await history_tvl_weekly(end_date, start_date_monthly);
        tvl_store = await models.Tvl_data_Monthly.create(
            oven_tvl = round(tvl_data['avg_tvl_data'], 6),
            amm_tvl = round(tvl_data['avg_amm_tvl_data'], 6),
            timestamp_from = start_date_monthly,
            timestamp_to = end_date,
            epoch_timestamp_from = int(start_date_monthly.timestamp()*1000),
            epoch_timestamp_to = int(end_date.timestamp()*1000)
        ) 

    ctx.logger.info("Hey Man, how are you")