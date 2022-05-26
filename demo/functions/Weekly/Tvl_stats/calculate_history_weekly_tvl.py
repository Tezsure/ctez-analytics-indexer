from audioop import avg
from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def history_tvl_weekly(start_date, ago_timestamp):
    try:
        tvl_data = await models.Tvl_data\
            .filter(timestamp__gte = ago_timestamp)\
            .filter(timestamp__lte = start_date)\
        
        avg_tvl = Decimal(0);

        for i in range(len(tvl_data)):
            avg_tvl = Decimal(Decimal(avg_tvl) + Decimal(tvl_data[i].tvl));
    
        if len(tvl_data)==0:
            avg_tvl = 0;
        else:
           avg_tvl = Decimal(avg_tvl/len(tvl_data));

    except(TypeError, AttributeError):
        avg_tvl = Decimal(0);
    
    return avg_tvl;     