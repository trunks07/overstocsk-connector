import aiohttp

from fastapi import FastAPI, APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.services.OverstocksService import OverstocksService

router = APIRouter()

@router.get("/sync-inventory")
async def syncIventory():
    try:
        response = await OverstocksService.callSyncInventory()

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": response}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)