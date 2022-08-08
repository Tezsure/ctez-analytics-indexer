
from decimal import Decimal
from demo.types.ctez_admin.big_map.ovens_value import OvensValue
from dipdup.models import BigMapDiff
from dipdup.context import HandlerContext
from demo.types.ctez_admin.big_map.ovens_key import OvensKey
from demo import models as models
import demo.models as models

async def on_oven_update(
    ctx: HandlerContext,
    ovens: BigMapDiff[OvensKey, OvensValue],
) -> None:
    
    # ctx.logger.info("Hey %s", ovens.data.timestamp.timestamp());
    if not ovens.value:
        # ctx.logger.info("Hey babe")
        return;

    # ctx.logger.info("Hey %s", data['total_supply'])
    
    tez = round(float(float(ovens.value.tez_balance)/(10 ** 6)), 6);
    ctez = round(float(float(ovens.value.ctez_outstanding)/(10 ** 6)), 6)
    
    oven_stats = await models.ovendata.update_or_create(
        oven_address = ovens.value.address,
        defaults={
            "ctez_standing": ctez,
            "tez_standing": tez,
            "timestamp": ovens.data.timestamp,
            "epoch_timestamp" : int(ovens.data.timestamp.timestamp()*1000)
        }
    )
    
    ovens_data = await models.ovendata\
          .all();
          
    tez_in_ovens = float(0);
    ctez_in_ovens = float(0);
    
    for i in range(len(ovens_data)):
        tez_in_ovens+=float(ovens_data[i].tez_standing);
        ctez_in_ovens+=float(ovens_data[i].ctez_standing);
        
    collateral = float(0);

    if ctez_in_ovens != 0:
        collateral = round(float(float(tez_in_ovens/ctez_in_ovens)*100), 6);

    tez_ovens = await models.TezOven.create(
        tez_in_all_ovens = tez_in_ovens,
        ctez_in_all_ovens = ctez_in_ovens,
        collateral_supply = collateral,
        timestamp = ovens.data.timestamp,
        epoch_timestamp = int(ovens.data.timestamp.timestamp()*1000)
    )
    
    