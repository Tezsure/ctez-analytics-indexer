
from dipdup.context import HookContext
from datetime import datetime, timedelta
import demo.models as models
from demo.functions.Main_stats.history_main import history_main_data
from demo.functions.Main_stats.main_history import main_history_data
from dateutil.relativedelta import *
from demo.functions.Weekly.Main_data_stats.calculate_history_weekly_monthly_maindata import history_main_data_weekly_monthly;

async def calculate_history_main_data(
    ctx: HookContext,
    major: bool,
) -> None:
    start_date = datetime(2022, 2, 1);
    start_date_monthly = datetime(2022, 2, 1);
    iteration = timedelta(hours=24);
    end_date = datetime.utcnow();
    iteration_month = relativedelta(months=+1)
    while start_date<=end_date:
        data = await history_main_data(start_date);

        if data == 0:
            data = await main_history_data();

        mainpage =  await models.MainDataRegularize.create(
        current_target = round(float(data.current_target), 5),
        current_price = round(float(data.current_price), 5),
        premium = round(float(data.premium), 5),
        current_annual_drift = round(float(data.current_annual_drift), 5),
        timestamp = start_date,  
        )
        start_date+=iteration;
    
    # Monthly Data

    while start_date_monthly<=end_date:
        month_ago_time = start_date_monthly - iteration_month;
        main_data = await history_main_data_weekly_monthly(start_date_monthly, month_ago_time);
        # print(tvl_data);
        main_stats = await models.MainDataRegularize_monthly.create(
            current_price = round(main_data['current_avg_price'], 5),
            current_target = round(main_data['current_avg_target'], 5),
            premium = round(main_data['current_avg_premium'], 5),
            current_annual_drift = round(main_data['current_avg_annual_drift'], 5),
            timestamp_from = month_ago_time,
            timestamp_to = start_date_monthly
        ) 
        start_date_monthly+=iteration_month
    
    if start_date_monthly!=end_date:
        start_date_monthly -= iteration_month;
        main_data = await history_main_data_weekly_monthly(end_date, start_date_monthly);
        main_stats = await models.MainDataRegularize_monthly.create(
            current_price = round(main_data['current_avg_price'], 5),
            current_target = round(main_data['current_avg_target'], 5),
            premium = round(main_data['current_avg_premium'], 5),
            current_annual_drift = round(main_data['current_avg_annual_drift'], 5),
            timestamp_from = start_date_monthly,
            timestamp_to = end_date
        )
        
    
    ctx.logger.info("Hey Man, How are you")
        
    