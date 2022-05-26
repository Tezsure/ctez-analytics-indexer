from decimal import Decimal
import imp
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def main_history_data():
    try:
        main_data = await models.MainData\
            .all()\
            .order_by("-timestamp")\
            .first()
    except(TypeError, AttributeError):
        main_data = Decimal(0);
    
    return main_data;     