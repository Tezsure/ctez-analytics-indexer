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
        avg_amm_tvl = Decimal(0);

        for i in range(len(tvl_data)):
            avg_tvl = Decimal(Decimal(avg_tvl) + Decimal(tvl_data[i].oven_tvl));
            avg_amm_tvl = Decimal(Decimal(avg_amm_tvl) + Decimal(tvl_data[i].amm_tvl));
    
        if len(tvl_data)==0:
            avg_tvl = 0;
            avg_amm_tvl = 0;
        else:
           avg_tvl = Decimal(avg_tvl/len(tvl_data));
           avg_amm_tvl = Decimal(avg_amm_tvl/len(tvl_data));

    except(TypeError, AttributeError):
        avg_tvl = Decimal(0);
        avg_amm_tvl = Decimal(0);

    ans = {};
    ans['avg_tvl_data'] = avg_tvl;
    ans['avg_amm_tvl_data'] = avg_amm_tvl;
    
    return ans;      