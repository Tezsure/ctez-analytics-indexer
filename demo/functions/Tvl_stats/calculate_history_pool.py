from decimal import Decimal
from multiprocessing import pool
from pyexpat import model
import demo.models as models

async def history_pool(start_date):
    try:
        pool_data = await models.Position\
            .filter(timestamp__gte=start_date)\
            .order_by("timestamp")\
            .first()
        pool_stats = Decimal(pool_data.quantity_pool1);

    except(TypeError, AttributeError):
        pool_stats = Decimal(0);
    
    return pool_stats;     