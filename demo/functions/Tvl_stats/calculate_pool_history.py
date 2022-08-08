from decimal import Decimal
from multiprocessing import pool
from pyexpat import model
import demo.models as models

async def pool_history():
    try:
        pool_data = await models.PoolsData\
            .all()\
            .order_by("-timestamp")\
            .first()
            
        pool_stats = Decimal(pool_data.quantity_pool1);
        print("Hey Women")
        # print("Hey", tvl_stat);

    except(TypeError, AttributeError):
        print("Errory Women1")
        pool_stats = Decimal(0);
    
    return pool_stats;     