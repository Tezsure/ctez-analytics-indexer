from decimal import Decimal
from pyexpat import model
import demo.models as models

async def history_price(start_date):
    try:
        ctez_trade = await models.Trade\
            .filter(timestamp__gte=start_date)\
            .order_by("timestamp")\
            .first()
        history_ctez_price = float(ctez_trade.price);
    except(TypeError, AttributeError):
        history_ctez_price = float(0);
    
    return history_ctez_price;        