from audioop import avg
from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def history_price_weekly_monthly(start_date, ago_timestamp):
    try:
        price_data = await models.pricestats\
            .filter(timestamp__gte = ago_timestamp)\
            .filter(timestamp__lte = start_date)\
        
        avg_ctez_price = Decimal(0);
        avg_tez_price = Decimal(0);

        for i in range(len(price_data)):
            avg_ctez_price = Decimal(Decimal(avg_ctez_price) + Decimal(price_data[i].ctez_price))
    
        if len(price_data)==0:
            avg_ctez_price = 0;
        else:
           avg_ctez_price = Decimal(avg_ctez_price/len(price_data));

    except(TypeError, AttributeError):
        print("Errory")
        avg_ctez_price = Decimal(0);
    
    ans = {};
    ans['current_avg_ctez_price'] = avg_ctez_price;
    return ans; 