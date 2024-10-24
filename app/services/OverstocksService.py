from app.libs.api import Overstocks
from app.libs.helper import weekDate, monthDates, timeZoneTimeStamp

class OverstocksService:
    async def callSyncInventory():
        params = "/overstock/inventory-sync"

        response = await Overstocks.GET(params)

        return response