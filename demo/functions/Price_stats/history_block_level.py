from decimal import Decimal
import imp
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def get_history_level(start_date):
    try:
        ctez_trade = await models.Trade\
            .filter(token_symbol = 'ctez')\
            .filter(timestamp__gte=start_date)\
            .order_by("timestamp")\
            .first()
        level_value = ctez_trade.level;
    except(TypeError, AttributeError):
        level_value = float(1);
    
    return level_value;            