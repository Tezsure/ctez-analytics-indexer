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
import math

async def on_cash_to_token(
    ctx: HandlerContext,
    cash_to_token: Transaction[CashToTokenParameter, CtezSwapStorage],
    cfmm_price: Transaction[CfmmPriceParameter, CtezAdminStorage],
    transfer: Transaction[TransferParameter, CtezMainStorage],
) -> None:
    # ctx.logger.info("Hey %s", cash_to_token)
    # ctx.logger.info("Hey %s", models.TradeSide.BUY);
    tez = float(cash_to_token.data.amount)/(10 ** 6);
    # ctx.logger.info("Hey %s", tez);
    token = float(transfer.parameter.value)/(10 ** 6);
    price_tez = 0;
    tez_pool = float(cash_to_token.storage.cashPool)/(10 ** 6);
    token_pool = float(cash_to_token.storage.tokenPool)/(10 ** 6);    
    if token == 0:
        return;
          
    price_tez = float(tez/token);
    symbol = "ctez"
    
    trade = models.Trade(
          token_symbol = symbol,
          trader = cash_to_token.parameter.to,
          operation_hash = cash_to_token.data.hash,
          side_trade = models.TradeSide.BUY,
          tez_qty = round(tez, 6),
          token_qty = round(token, 6),
          price = round(price_tez, 6),
          level = cash_to_token.data.level,
          timestamp = cash_to_token.data.timestamp,
          epoch_timestamp = int(cash_to_token.data.timestamp.timestamp()*1000)
    )
    
    await trade.save();

    pools = models.PoolsData(
        quantity_pool1 = round(tez_pool, 6),
        quantity_pool2 = round(token_pool, 6),
        timestamp = cash_to_token.data.timestamp,
        epoch_timestamp = int(cash_to_token.data.timestamp.timestamp()*1000)
    );
    await pools.save();

    # ctx.logger.info("Hey %s", cfmm_price);
    target = float(float(cfmm_price.storage.target)/(2 ** 48));
    price = float(float(cash_to_token.storage.cashPool)/float(cash_to_token.storage.tokenPool));
    premium_val = (float(price/target) - float(1.0));
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