from decimal import Decimal
from pyexpat import model
import demo.models as models

async def tvl_history():
    try:
        tvl_data = await models.TezOven\
            .all()\
            .order_by("-timestamp")\
            .first()
        
        print(tvl_data.tez_in_all_ovens)
        tvl_stats = Decimal(tvl_data.tez_in_all_ovens);
        # print("Hey", tvl_stat);
        print("Hey Man")

    except(TypeError, AttributeError):
        print("Errory Man1")
        tvl_stats = Decimal(0);
    
    return tvl_stats;     