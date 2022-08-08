
from email.policy import default
from demo.types.ctez_main.storage import CtezMainStorage
from demo.types.ctez_admin.storage import CtezAdminStorage
from dipdup.models import Transaction
from dipdup.context import HandlerContext
from demo.types.ctez_main.parameter.mint_or_burn import MintOrBurnParameter
from demo.types.ctez_admin.parameter.liquidate import LiquidateParameter
import demo.models as models

async def on_liquidate(
    ctx: HandlerContext,
    liquidate: Transaction[LiquidateParameter, CtezAdminStorage],
    mint_or_burn: Transaction[MintOrBurnParameter, CtezMainStorage],
) -> None:
    # ctx.logger.info("Hey %s", liquidate.storage.ovens[0].value);
    
    oven = await models.ovendata.update_or_create(
        oven_address = liquidate.storage.ovens[0].value.address,
        defaults={
            'liquidation' : True
        }
    )

    # liquidated = await models.Ovens_liquidated.get_or_create(
    #     id = 1,
    #     defaults={
    #         "number_of_ovens_liquidated":-1,
    #     }
    # );


    # ctx.logger.info("Hey %s", liquidated[0].number_of_ovens_liquidated);

    ovens_liquidated = await models.Ovens_liquidated.update_or_create(
        liquidated_oven = liquidate.storage.ovens[0].value.address,
    );

    supply = round(float(mint_or_burn.storage.total_supply)/(10**6), 6);
    supply_data = await models.Supply.update_or_create(
        id = 1,
        defaults={
            'total_supply':supply
        }
    )