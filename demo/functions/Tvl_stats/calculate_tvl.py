from decimal import Decimal
from pyexpat import model
import demo.models as models

async def tvl_stats():
    try:
        oven_stat = await models.ovendata\
            .all()
        tvl_stat = Decimal(0);
        for i in range(len(oven_stat)):
            tvl_stat += Decimal(oven_stat[i].tez_standing);

    except(TypeError, AttributeError):
        tvl_stat = Decimal(0);
    
    return tvl_stat;     