from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import timedelta, datetime

async def buy_sell_volume_percentage(buy_sell_volume, token_volume):
    try:
        
        buy_sell_volume = float(float(float(buy_sell_volume)/float(token_volume))*100);
    except(TypeError, AttributeError, ZeroDivisionError, ValueError):
        buy_sell_volume = float(0);
    
    return buy_sell_volume;
    