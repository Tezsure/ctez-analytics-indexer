from decimal import Decimal
from pyexpat import model
import demo.models as models

async def history_tvl(start_date):
    try:
        tvl_data = await models.TezOven\
            .filter(timestamp__gte=start_date)\
            .order_by("timestamp")\
            .first()
        # print(tvl_data);
        tvl_stats = Decimal(tvl_data.tez_in_all_ovens);
        # print("Hey", tvl_stat);

    except(TypeError, AttributeError):
        # print("Errory Man")
        tvl_stats = Decimal(0);
    
    return tvl_stats;     