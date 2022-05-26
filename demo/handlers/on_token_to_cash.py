
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

async def on_token_to_cash(
    ctx: HandlerContext,
    token_to_cash: Transaction[TokenToCashParameter, CtezSwapStorage],
    cfmm_price: Transaction[CfmmPriceParameter, CtezAdminStorage],
    transfer: Transaction[TransferParameter, CtezMainStorage],
    transaction_3: OperationData,
) -> None:
    tez = float(transaction_3.amount)/(10 ** 6);
    token = float(token_to_cash.parameter.tokensSold)/(10 ** 6);
    if tez == 0:
        return;
    price_tez = float(tez/token);
    symbol = "ctez";
    
    trade = models.Trade(
          token_symbol = symbol,
          trader = token_to_cash.parameter.to,
          side_trade = models.TradeSide.SELL,
          tez_qty = round(tez, 5),
          token_qty = round(token, 5),
          price = round(price_tez, 5),
          level = token_to_cash.data.level,
          timestamp = token_to_cash.data.timestamp
    )
    
    await trade.save();
    
    target = float(float(cfmm_price.storage.target)/(2 ** 48));
    price = float(float(token_to_cash.storage.cashPool)/float(token_to_cash.storage.tokenPool));
    premium_val = float(price/target) - float(1.0);
    
    mainpage =  await models.MainData.create(
        current_target = round(target, 5),
        current_price = round(price, 5),
        premium = round(premium_val, 5),
        current_annual_drift = round(float(cfmm_price.storage.drift), 5),
        timestamp = cfmm_price.data.timestamp,  
    )

    supply = round(float(transfer.storage.total_supply)/(10**6), 5);
    supply_data = await models.Supply.update_or_create(
        id = 1,
        defaults={
            'total_supply':supply
        }
    )