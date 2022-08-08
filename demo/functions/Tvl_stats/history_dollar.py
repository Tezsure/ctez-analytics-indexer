from decimal import Decimal
from pyexpat import model
import demo.models as models

async def history_dollar_stats():
    try:
        Usd_stats = await models.Token_USD\
            .all()\
            .order_by("-timestamp")\
            .first()
        
        dollar = Decimal(Usd_stats.price);

    except(TypeError, AttributeError):
        print("Errory Dollar1")
        dollar = Decimal(0);
    
    return dollar;     