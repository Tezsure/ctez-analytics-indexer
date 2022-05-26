from decimal import Decimal
from pyexpat import model
import demo.models as models

async def price_stats_provider():
    try:
        ctez_trade = await models.Trade\
            .filter(token_symbol='ctez')\
            .order_by("-timestamp")\
            .first()
        # print(ctez_trade.price);
        ctez_price = float(ctez_trade.price);
    except(TypeError, AttributeError):
        ctez_price = float(0);
    
    return ctez_price;        