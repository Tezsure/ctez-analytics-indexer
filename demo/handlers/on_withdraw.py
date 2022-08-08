
from demo.types.ctez_admin.parameter.withdraw import WithdrawParameter
from dipdup.models import Transaction
from dipdup.context import HandlerContext
from demo.types.ctez_admin.storage import CtezAdminStorage
import demo.models as models

async def on_withdraw(
    ctx: HandlerContext,
    withdraw: Transaction[WithdrawParameter, CtezAdminStorage],
) -> None:
    withdraw_data = await models.Deposit_Withdraw_Data.create(
        address = withdraw.parameter.to,
        oven_address = withdraw.storage.ovens[0].value.address,
        operation_hash = withdraw.data.hash,
        side_oven = models.OvenSide.Withdraw,
        target = round(float(float(withdraw.storage.target)/(2 ** 48)), 6),
        amount = round(float(withdraw.parameter.amount)/ (10 ** 6), 6),
        timestamp = withdraw.data.timestamp,
        epoch_timestamp = int(withdraw.data.timestamp.timestamp()*1000)
    )