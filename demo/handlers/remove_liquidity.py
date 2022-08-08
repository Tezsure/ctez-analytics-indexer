
from demo.types.ctez_swap.parameter.remove_liquidity import RemoveLiquidityParameter
from dipdup.context import HandlerContext
from dipdup.models import Transaction
from demo.types.ctez_swap.storage import CtezSwapStorage
from dipdup.models import OperationData
from demo.types.ctez_main.parameter.transfer import TransferParameter
from demo.types.ctez_lp.storage import CtezLpStorage
from demo.types.ctez_main.storage import CtezMainStorage
from demo.types.ctez_lp.parameter.mint_or_burn import MintOrBurnParameter
from decimal import Decimal
import demo.models as models

async def remove_liquidity(
    ctx: HandlerContext,
    remove_liquidity: Transaction[RemoveLiquidityParameter, CtezSwapStorage],
    mint_or_burn: Transaction[MintOrBurnParameter, CtezLpStorage],
    transfer: Transaction[TransferParameter, CtezMainStorage],
    transaction_3: OperationData,
) -> None:
    tez_qty = float(transaction_3.amount)/(10 ** 6);
    token_qty = float(transfer.parameter.value)/(10 ** 6);
    tez_pool = float(remove_liquidity.storage.cashPool)/(10 ** 6)
    token_pool = float(remove_liquidity.storage.tokenPool)/(10 ** 6);
    price_qty = Decimal(tez_pool/token_pool);
    burn_qty = -float(mint_or_burn.parameter.quantity)/(10 ** 6);
    
    position = models.Position(
        token_symbol = 'ctez',
        trader = remove_liquidity.parameter.to,
        operation_hash = remove_liquidity.data.hash,
        side_liquidity = models.LiquiditySide.REMOVE,
        quantity_tk1 = round(tez_qty, 6),
        quantity_tk2 = round(token_qty, 6),
        quantity_mint = 0,
        quantity_burn = round(burn_qty, 6),
        quantity_pool1 = round(tez_pool, 6),
        quantity_pool2 = round(token_pool, 6),
        price = round(price_qty, 6),
        level = remove_liquidity.data.level,
        timestamp = remove_liquidity.data.timestamp,
        epoch_timestamp = int(remove_liquidity.data.timestamp.timestamp()*1000)
    )
    await position.save();

    pools = models.PoolsData(
        quantity_pool1 = round(tez_pool, 6),
        quantity_pool2 = round(token_pool, 6),
        timestamp = remove_liquidity.data.timestamp,
        epoch_timestamp = int(remove_liquidity.data.timestamp.timestamp()*1000)
    );
    await pools.save();

    supply = round(float(mint_or_burn.storage.total_supply)/(10**6), 6);
    supply_data = await models.Supply.update_or_create(
        id = 1,
        defaults={
            'total_supply':supply
        }
    )