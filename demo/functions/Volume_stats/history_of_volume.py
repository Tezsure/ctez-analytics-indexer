from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import timedelta

async def history_volume_days(start_date, days):
    range_date = start_date - timedelta(days);
    try:
        token_stats = await models.pricestats\
            .filter(timestamp__lte = start_date)\
            .order_by("-timestamp")\
            .first()
        
        token_price = Decimal(token_stats.ctez_price);
        token_trades = await models.Trade\
            .filter(timestamp__gte = range_date)\
            .filter(timestamp__lte = start_date)\
                
        volume = Decimal(0.0001);
        for i in range(len(token_trades)):
            volume += Decimal(token_trades[i].token_qty);
        
        volume_token = Decimal(volume*token_price);
    except(TypeError, AttributeError):
        volume_token = Decimal(1);
    
    return volume_token;    