from audioop import avg
from decimal import Decimal
from pyexpat import model
import demo.models as models
from datetime import datetime, timedelta

async def history_volume_monthly(start_date, ago_timestamp):
    try:
        volume_data = await models.volumestats\
            .filter(timestamp__gte = ago_timestamp)\
            .filter(timestamp__lte = start_date)\
        
        avg_volume = Decimal(0);

        for i in range(len(volume_data)):
            avg_volume = Decimal(Decimal(avg_volume) + Decimal(volume_data[i].volume_24hours));
    
        if len(volume_data)==0:
            avg_volume = 0;
        else:
           avg_volume = Decimal(avg_volume/len(volume_data));

    except(TypeError, AttributeError):
        print("Errory Babe")
        avg_volume = Decimal(0);
    
    return avg_volume;     