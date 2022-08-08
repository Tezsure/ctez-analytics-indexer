
from tokenize import Double
from demo import models as models
from demo.types.oracle_main.big_map.asset_map_key import AssetMapKey
from dipdup.models import BigMapDiff
from demo.types.oracle_main.big_map.asset_map_value import AssetMapValue
from dipdup.context import HandlerContext
import demo.models as models
from decimal import Decimal
from datetime import datetime
import pytz

utc=pytz.UTC

async def on_asset_update(
    ctx: HandlerContext,
    asset_map: BigMapDiff[AssetMapKey, AssetMapValue],
) -> None:
    start_date = datetime(2022, 1, 1);
    start_date = utc.localize(start_date);
    if asset_map.data.timestamp < start_date:
        return;
    if not asset_map.key:
        return;
    # ctx.logger.info("Hey %s", asset_map.value.computedPrice);
    if asset_map.key.__root__ == "XTZ-USD":
        # ctx.logger.info("hey %s", asset_map.key.__root__)
        price = float(asset_map.value.computedPrice)/(10 ** 6);
        usd_data = await models.Token_USD.create(
                price = round(price, 6),
                timestamp = asset_map.data.timestamp,
                epoch_timestamp = int(asset_map.data.timestamp.timestamp()*1000)
        );
        
        
        
        
        
        