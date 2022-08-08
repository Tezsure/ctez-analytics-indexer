from decimal import Decimal
from multiprocessing import pool
from pyexpat import model
import demo.models as models

async def ctez_pool_history():
    try:
        pool_data = await models.PoolsData\
            .all()\
            .order_by("-timestamp")\
            .first()
            
        pool_stats = Decimal(pool_data.quantity_pool2);

    except(TypeError, AttributeError):
        pool_stats = Decimal(0);
    
    return pool_stats;     