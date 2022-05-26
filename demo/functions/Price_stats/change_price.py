from decimal import Decimal
import imp
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def price_change_stats(price_token, amount_of_days):
    current_timestamp = datetime.utcnow();
    days_ago_time = current_timestamp - timedelta(days=amount_of_days);
    try:
        ctez_trade = await models.Trade\
            .filter(timestamp__gte=days_ago_time)\
            .filter(timestamp__lte=current_timestamp)\
            .order_by("timestamp")\
            .first()
        ctez_price_days_ago = float(ctez_trade.price);
        
        price_change = float(((price_token - ctez_price_days_ago)/ctez_price_days_ago)*100);
        # print("Hey", price_change);
        
    except(TypeError, AttributeError):
        price_change = float(0);
    
    return price_change;            