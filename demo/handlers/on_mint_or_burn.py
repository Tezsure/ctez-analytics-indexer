
from demo.types.ctez_main.storage import CtezMainStorage
from demo.types.ctez_main.parameter.mint_or_burn import MintOrBurnParameter
from demo.types.ctez_admin.parameter.mint_or_burn import MintOrBurnParameter
from dipdup.context import HandlerContext
from demo.types.ctez_admin.storage import CtezAdminStorage
from dipdup.models import Transaction
import demo.models as models

async def on_mint_or_burn(
    ctx: HandlerContext,
    mint_or_burn_0: Transaction[MintOrBurnParameter, CtezAdminStorage],
    mint_or_burn_1: Transaction[MintOrBurnParameter, CtezMainStorage],
) -> None:
    # ctx.logger.info("Hey babe %s", mint_or_burn_0.storage);
    mint = 0;
    burn = 0;
    quantity = float(mint_or_burn_0.parameter.quantity)/(10 ** 6);

    target = float(float(mint_or_burn_0.storage.target)/(2 ** 48));

    if quantity<0:
        burn = (-quantity);
    else:
        mint = (quantity);
        
    data = await models.Mint_Burn_Data.create(
        address = mint_or_burn_0.storage.ovens[0].key.owner,
        oven_address = mint_or_burn_0.storage.ovens[0].value.address,
        target = round(target, 5),
        mint_amount = round(mint, 5),
        burn_amount = round(burn, 5),
        timestamp = mint_or_burn_0.data.timestamp
    );
    
    supply = round(float(mint_or_burn_1.storage.total_supply)/(10**6), 5);
    supply_data = await models.Supply.update_or_create(
        id = 1,
        defaults={
            'total_supply':supply
        }
    )