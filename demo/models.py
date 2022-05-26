from email.policy import default
from tortoise import Model, fields
from enum import IntEnum

class TradeSide(IntEnum):
    BUY = 1
    SELL = 0
    
class LiquiditySide(IntEnum):
    ADD = 1
    REMOVE = 0

class OvenSide(IntEnum):
    Deposit = 1
    Withdraw = 0


class Trade(Model):
    id = fields.IntField(pk=True)
    token_symbol = fields.CharField(max_length=7)
    trader = fields.CharField(max_length=36)
    side_trade = fields.IntEnumField(enum_type=TradeSide)
    tez_qty = fields.FloatField();
    token_qty = fields.FloatField();
    price = fields.FloatField();
    level = fields.BigIntField();
    timestamp = fields.DatetimeField()
    
class Position(Model):
    id = fields.IntField(pk=True)
    token_symbol = fields.CharField(max_length=7)
    trader = fields.CharField(36)
    side_liquidity = fields.IntEnumField(enum_type=LiquiditySide)
    quantity_tk1 = fields.FloatField();
    quantity_tk2 = fields.FloatField();
    quantity_mint = fields.FloatField();
    quantity_burn = fields.FloatField();
    quantity_pool1 = fields.FloatField();
    quantity_pool2 = fields.FloatField();
    price = fields.FloatField();
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()
    
class MainData(Model):
    id = fields.IntField(pk=True)
    current_target = fields.DecimalField(max_digits=40, decimal_places=7);
    current_price = fields.DecimalField(max_digits=40, decimal_places=7);
    premium = fields.DecimalField(max_digits=40, decimal_places=7);
    current_annual_drift = fields.DecimalField(max_digits=40, decimal_places=7);
    timestamp = fields.DatetimeField()
    
class MainDataRegularize(Model):
    id = fields.IntField(pk=True)
    current_target = fields.FloatField();
    current_price = fields.FloatField();
    premium = fields.FloatField();
    current_annual_drift = fields.FloatField();
    timestamp = fields.DatetimeField()
    
class MainDataRegularize_monthly(Model):
    id = fields.IntField(pk=True)
    current_target = fields.FloatField();
    current_price = fields.FloatField();
    premium = fields.FloatField();
    current_annual_drift = fields.FloatField();
    timestamp_from = fields.DatetimeField()
    timestamp_to = fields.DatetimeField()

class pricestats(Model):
    id = fields.IntField(pk=True)
    token_symbol = fields.CharField(max_length=7)
    ctez_price = fields.FloatField();
    tez_price = fields.FloatField();
    price_change_24hours = fields.FloatField();
    price_change_7days = fields.FloatField();
    prce_change_1month = fields.FloatField();
    price_change_1year = fields.FloatField();
    level = fields.BigIntField();
    timestamp = fields.DatetimeField()

class pricestats_monthly(Model):
    id = fields.IntField(pk=True)
    token_symbol = fields.CharField(max_length=7)
    ctez_price = fields.FloatField();
    tez_price = fields.FloatField();
    timestamp_from = fields.DatetimeField()
    timestamp_to = fields.DatetimeField()


class volumestats(Model):
    id = fields.IntField(pk=True)
    token_symbol = fields.CharField(max_length=7)
    volume_24hours = fields.FloatField();
    buy_volume = fields.FloatField();
    sell_volume = fields.FloatField();
    buy_volume_percentage_24hours = fields.FloatField();
    sell_volume_percentage_24hours = fields.FloatField();
    volume_7days = fields.FloatField();
    volume_1month = fields.FloatField();
    level = fields.BigIntField()
    timestamp = fields.DatetimeField()    

class volumestats_monthly(Model):
    id = fields.IntField(pk=True)
    token_symbol = fields.CharField(max_length=7)
    volume = fields.FloatField();
    timestamp_from = fields.DatetimeField()
    timestamp_to = fields.DatetimeField()   
    
class ovendata(Model):
    id = fields.IntField(pk=True);
    oven_address = fields.CharField(max_length=36);
    ctez_standing = fields.FloatField();
    tez_standing = fields.FloatField();
    liquidation = fields.BooleanField(default=False);
    timestamp = fields.DatetimeField();
    
class TezOven(Model):
    id = fields.IntField(pk=True);
    tez_in_all_ovens = fields.BigIntField();
    ctez_in_all_ovens = fields.BigIntField();
    collateral_supply = fields.FloatField();
    timestamp = fields.DatetimeField();

class Mint_Burn_Data(Model):
    id = fields.IntField(pk=True);
    address = fields.CharField(36);
    oven_address = fields.CharField(36);
    target = fields.FloatField();
    mint_amount = fields.FloatField();
    burn_amount = fields.FloatField();
    timestamp = fields.DatetimeField();

class Deposit_Withdraw_Data(Model):
    id = fields.IntField(pk=True);
    address = fields.CharField(36);
    oven_address = fields.CharField(36);
    side_oven = fields.IntEnumField(enum_type=OvenSide)
    target = fields.FloatField();
    amount = fields.FloatField();
    timestamp = fields.DatetimeField();
    
class Tvl_data(Model):
    id = fields.IntField(pk=True);
    tvl = fields.FloatField();
    timestamp = fields.DatetimeField();

class Tvl_data_Monthly(Model):
    id = fields.IntField(pk=True);
    tvl = fields.FloatField();
    timestamp_from = fields.DatetimeField();
    timestamp_to = fields.DatetimeField();
    
class Token_USD(Model):
    id = fields.IntField(pk=True);
    price = fields.FloatField();
    timestamp = fields.DatetimeField();

class Ovens_liquidated(Model):
    id = fields.IntField(pk=True);
    liquidated_oven = fields.CharField(36);

class Supply(Model):
    id = fields.IntField(pk=True);
    total_supply = fields.FloatField();
    
    