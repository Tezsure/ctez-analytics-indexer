from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import timedelta, datetime

async def volume_days(days):
    timestamp_now = datetime.utcnow();
    timestamp_daysago = timestamp_now - timedelta(days)
    
    
    try:
        token_stats = await models.pricestats\
            .filter(token_symbol='ctez')\
            .order_by("-timestamp")\
            .first()
        token_price = float(token_stats.ctez_price);
        token_trades = await models.Trade\
            .filter(timestamp__gte = timestamp_daysago)\
            .filter(timestamp__lte = timestamp_now)\
                
        volume = float(0.0001);
        for i in range(len(token_trades)):
            volume += float(token_trades[i].token_qty);
        
        volume_token = float(volume*token_price);
    except(TypeError, AttributeError):
        volume_token = float(0);
    
    return volume_token;    