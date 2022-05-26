from demo.types.ctez_swap.storage import CtezSwapStorage
from demo.types.ctez_main.storage import CtezMainStorage
from demo.types.ctez_main.parameter.transfer import TransferParameter
from demo.types.ctez_admin.parameter.cfmm_price import CfmmPriceParameter
from dipdup.models import Transaction
from demo.types.ctez_swap.parameter.cash_to_token import CashToTokenParameter
from dipdup.context import HandlerContext
from demo.types.ctez_admin.storage import CtezAdminStorage
import demo.models as models
from decimal import Decimal

async def on_cash_to_token(
    ctx: HandlerContext,
    cash_to_token: Transaction[CashToTokenParameter, CtezSwapStorage],
    cfmm_price: Transaction[CfmmPriceParameter, CtezAdminStorage],
    transfer: Transaction[TransferParameter, CtezMainStorage],
) -> None:
    tez = float(cash_to_token.data.amount)/(10 ** 6);
    token = float(transfer.parameter.value)/(10 ** 6);
    price_tez = 0;
    if token == 0:
        return;
          
    price_tez = float(tez/token);
    symbol = "ctez"
    
    trade = models.Trade(
          token_symbol = symbol,
          trader = cash_to_token.parameter.to,
          side_trade = models.TradeSide.BUY,
          tez_qty = round(tez, 5),
          token_qty = round(token, 5),
          price = round(price_tez, 5),
          level = cash_to_token.data.level,
          timestamp = cash_to_token.data.timestamp
    )
    
    await trade.save();
    target = float(float(cfmm_price.storage.target)/(2 ** 48));
    price = float(float(cash_to_token.storage.cashPool)/float(cash_to_token.storage.tokenPool));
    premium_val = (float(price/target) - float(1.0));
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