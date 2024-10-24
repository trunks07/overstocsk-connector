import aiohttp

from fastapi import APIRouter, HTTPException, status

router = APIRouter()

@router.get("/")
async def index():
    try:
        return {"status": status.HTTP_200_OK, "message": "Welcome to MKTA Marketplace connector micro service!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"System un-healthy! Error: {str(e)}")

# System health check
@router.get("/healthz")
async def healthCheck():
    try:
        return {"status": status.HTTP_200_OK, "message": "System is healthy!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"System un-healthy! Error: {str(e)}")

@router.get("/ip-address")
async def getIpAddress():
    try:
        url = "https://api.ipify.org"
        body = {}
        headers = {}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=body, headers=headers) as resp:
                response = await resp.text()

        return {"status": status.HTTP_200_OK, "data": response}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"System Error: {str(e)}")