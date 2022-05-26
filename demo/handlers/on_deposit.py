
from demo.types.ctez_admin.storage import CtezAdminStorage
from dipdup.models import Transaction
from dipdup.context import HandlerContext
from demo.types.ctez_admin.parameter.register_deposit import RegisterDepositParameter
import demo.models as models
async def on_deposit(
    ctx: HandlerContext,
    register_deposit: Transaction[RegisterDepositParameter, CtezAdminStorage],
) -> None:
    # ctx.logger.info("Hey Man and Babe %s", register_deposit);
     
    #  target = ;
    
    deposit = await models.Deposit_Withdraw_Data.create(
        address = register_deposit.parameter.handle.owner,
        oven_address = register_deposit.storage.ovens[0].value.address,
        side_oven = models.OvenSide.Deposit,
        target = round(float(float(register_deposit.storage.target)/(2 ** 48)), 5),
        amount = round(float(register_deposit.parameter.amount)/(10 ** 6), 5),
        timestamp = register_deposit.data.timestamp
    )
