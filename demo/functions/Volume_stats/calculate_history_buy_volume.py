from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import timedelta, datetime

async def buy_volume_of_24hours_history(start_date):
    # timestamp_now = datetime.utcnow();
    timestamp_yesteraday = start_date - timedelta(hours=24)
    
    
    try:
        token_stats = await models.pricestats\
            .filter(token_symbol='ctez')\
            .filter(timestamp__gte = start_date)\
            .order_by("timestamp")\
            .first()
        token_price = float(token_stats.ctez_price);
        token_trades = await models.Trade\
            .filter(timestamp__gte = timestamp_yesteraday)\
            .filter(timestamp__lte = start_date)\
            .filter(side_trade=1)
                
        volume = float(0.0001);
        for i in range(len(token_trades)):
            volume += float(token_trades[i].token_qty);
        
        volume_token = float(volume*token_price);
    except(TypeError, AttributeError):
        volume_token = float(0);
    
    return volume_token;    