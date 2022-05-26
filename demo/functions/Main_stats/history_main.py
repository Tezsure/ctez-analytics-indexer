from decimal import Decimal
import imp
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def history_main_data(start_date):
    try:
        main_data = await models.MainData\
            .filter(timestamp__gte=start_date)\
            .order_by("timestamp")\
            .first()
        print("Hey Man", main_data.current_target);
    except(TypeError, AttributeError):
        # print("Errory")
        main_data = Decimal(0);
    
    return main_data;     