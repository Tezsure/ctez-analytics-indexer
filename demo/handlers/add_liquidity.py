
from demo.types.ctez_swap.storage import CtezSwapStorage
from demo.types.ctez_main.storage import CtezMainStorage
from demo.types.ctez_lp.storage import CtezLpStorage
from demo.types.ctez_main.parameter.transfer import TransferParameter
from dipdup.models import Transaction
from demo.types.ctez_lp.parameter.mint_or_burn import MintOrBurnParameter
from dipdup.context import HandlerContext
from demo.types.ctez_swap.parameter.add_liquidity import AddLiquidityParameter
from decimal import Decimal
import demo.models as models

async def add_liquidity(
    ctx: HandlerContext,
    add_liquidity: Transaction[AddLiquidityParameter, CtezSwapStorage],
    transfer: Transaction[TransferParameter, CtezMainStorage],
    mint_or_burn: Transaction[MintOrBurnParameter, CtezLpStorage],
) -> None:
    tez_qty = float(add_liquidity.data.amount)/(10 ** 6);
    token_qty = float(transfer.parameter.value)/(10 ** 6);
    tez_pool = float(add_liquidity.storage.cashPool)/(10 ** 6);
    token_pool = float(add_liquidity.storage.tokenPool)/(10 ** 6);
    price_qty = float(tez_pool/token_pool);
    mint_qty = Decimal(float(mint_or_burn.parameter.quantity)/(10 ** 6));
    
    position = models.Position(
        token_symbol = 'ctez',
        trader = add_liquidity.parameter.owner,
        operation_hash = add_liquidity.data.hash,
        side_liquidity = models.LiquiditySide.ADD,
        quantity_tk1 = round(tez_qty, 6),
        quantity_tk2 = round(token_qty, 6),
        quantity_mint = round(mint_qty, 6),
        quantity_burn = 0,
        quantity_pool1 = round(tez_pool, 6),
        quantity_pool2 = round(token_pool, 6),
        price = round(price_qty, 6),
        level = add_liquidity.data.level,
        timestamp = add_liquidity.data.timestamp,
        epoch_timestamp = int(add_liquidity.data.timestamp.timestamp()*1000)
    )
    await position.save();

    pools = models.PoolsData(
        quantity_pool1 = round(tez_pool, 6),
        quantity_pool2 = round(token_pool, 6),
        timestamp = add_liquidity.data.timestamp,
        epoch_timestamp = int(add_liquidity.data.timestamp.timestamp()*1000)
    );
    await pools.save();
    
    supply = round(float(mint_or_burn.storage.total_supply)/(10**6), 6);
    supply_data = await models.Supply.update_or_create(
        id = 1,
        defaults={
            'total_supply':supply
        }
    )