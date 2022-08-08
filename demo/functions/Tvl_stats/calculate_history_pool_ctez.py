from decimal import Decimal
from multiprocessing import pool
from pyexpat import model
import demo.models as models

async def history_pool_ctez(start_date):
    try:
        pool_data = await models.PoolsData\
            .filter(timestamp__gte=start_date)\
            .order_by("timestamp")\
            .first()
        # print(pool_data.quantity_pool1);
        pool_stats = Decimal(pool_data.quantity_pool2);
        # print("Hey", tvl_stat);

    except(TypeError, AttributeError):
        print("Errory Women")
        pool_stats = Decimal(0);
    
    return pool_stats;     