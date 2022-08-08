
from demo.types.ctez_admin.parameter.cfmm_price import CfmmPriceParameter
from dipdup.models import OperationData
from demo.types.ctez_swap.storage import CtezSwapStorage
from demo.types.ctez_swap.parameter.token_to_cash import TokenToCashParameter
from demo.types.ctez_main.storage import CtezMainStorage
from demo.types.ctez_main.parameter.transfer import TransferParameter
from dipdup.models import Transaction
from dipdup.context import HandlerContext
from demo.types.ctez_admin.storage import CtezAdminStorage
from decimal import Decimal
import demo.models as models
import math

async def on_token_to_cash(
    ctx: HandlerContext,
    token_to_cash: Transaction[TokenToCashParameter, CtezSwapStorage],
    cfmm_price: Transaction[CfmmPriceParameter, CtezAdminStorage],
    transfer: Transaction[TransferParameter, CtezMainStorage],
    transaction_3: OperationData,
) -> None:
    tez = float(transaction_3.amount)/(10 ** 6);
    token = float(token_to_cash.parameter.tokensSold)/(10 ** 6);
    tez_pool = float(token_to_cash.storage.cashPool)/(10 ** 6);
    token_pool = float(token_to_cash.storage.tokenPool)/(10 ** 6);
    if tez == 0:
        return;
    price_tez = float(tez/token);
    symbol = "ctez";
    
    trade = models.Trade(
          token_symbol = symbol,
          trader = token_to_cash.parameter.to,
          operation_hash = token_to_cash.data.hash,
          side_trade = models.TradeSide.SELL,
          tez_qty = round(tez, 5),
          token_qty = round(token, 5),
          price = round(price_tez, 5),
          level = token_to_cash.data.level,
          timestamp = token_to_cash.data.timestamp,
          epoch_timestamp = int(token_to_cash.data.timestamp.timestamp()*1000)
    )
    
    await trade.save();

    pools = models.PoolsData(
        quantity_pool1 = round(tez_pool, 6),
        quantity_pool2 = round(token_pool, 6),
        timestamp = token_to_cash.data.timestamp,
        epoch_timestamp = int(token_to_cash.data.timestamp.timestamp()*1000)
    );
    await pools.save();
    
    target = float(float(cfmm_price.storage.target)/(2 ** 48));
    price = float(float(token_to_cash.storage.cashPool)/float(token_to_cash.storage.tokenPool));
    premium_val = float(price/target) - float(1.0);
    drift = float((1 + float(cfmm_price.storage.drift) / 2 ** 48) ** (365.25 * 24 * 3600) - 1.0);
    mainpage =  await models.MainData.create(
        current_target = round(target, 6),
        current_price = round(price, 6),
        premium = round(premium_val, 6),
        current_annual_drift = round(drift, 6),
        timestamp = cfmm_price.data.timestamp,  
        epoch_timestamp = int(cfmm_price.data.timestamp.timestamp()*1000)
    )

    supply = round(float(transfer.storage.total_supply)/(10**6), 6);
    supply_data = await models.Supply.update_or_create(
        id = 1,
        defaults={
            'total_supply':supply
        }
    )