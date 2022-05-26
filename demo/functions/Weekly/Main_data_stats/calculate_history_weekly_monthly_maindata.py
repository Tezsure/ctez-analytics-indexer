from audioop import avg
from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def history_main_data_weekly_monthly(start_date, ago_timestamp):
    try:
        main_data = await models.MainDataRegularize\
            .filter(timestamp__gte = ago_timestamp)\
            .filter(timestamp__lte = start_date)\
        
        avg_price = Decimal(0);
        avg_target = Decimal(0);
        avg_premium = Decimal(0);
        avg_annual_drift = Decimal(0);
        
        for i in range(len(main_data)):
            avg_price = Decimal(Decimal(avg_price) + Decimal(main_data[i].current_price));
            avg_target = Decimal(Decimal(avg_target) + Decimal(main_data[i].current_target));
            avg_premium = Decimal(Decimal(avg_premium) + Decimal(main_data[i].premium));
            avg_annual_drift = Decimal(Decimal(avg_annual_drift) + Decimal(main_data[i].current_annual_drift));
    
        if len(main_data)==0:
            avg_price = Decimal(0);
            avg_target = Decimal(0);
            avg_premium = Decimal(0);
            avg_annual_drift = Decimal(0);
        else:
            avg_price = Decimal(avg_price/len(main_data));
            avg_target = Decimal(avg_target/len(main_data));
            avg_premium = Decimal(avg_premium/len(main_data));
            avg_annual_drift = Decimal(avg_annual_drift/len(main_data));

    except(TypeError, AttributeError):
        print("Errory")
        avg_price = Decimal(0);
        avg_target = Decimal(0);
        avg_premium = Decimal(0);
        avg_annual_drift = Decimal(0);

    ans = {};
    ans['current_avg_price'] = avg_price;
    ans['current_avg_target'] = avg_target;
    ans['current_avg_premium'] = avg_premium;
    ans['current_avg_annual_drift'] = avg_annual_drift;
    return ans; 