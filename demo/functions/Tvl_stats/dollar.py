from decimal import Decimal
from pyexpat import model
import demo.models as models

async def dollar_stats(start_date):
    try:
        Usd_stats = await models.Token_USD\
            .filter(timestamp__gte=start_date)\
            .order_by("timestamp")\
            .first()
        
        dollar = Decimal(Usd_stats.price);

    except(TypeError, AttributeError):
        dollar = Decimal(0);
    
    return dollar;     