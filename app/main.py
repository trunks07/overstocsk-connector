import asyncio
import uvicorn

from fastapi.responses import JSONResponse
from apscheduler.triggers.cron import CronTrigger
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import Depends, FastAPI, Request, status
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import System
from app.routers import Overstocks
from app.settings.environment import Env
from app.settings.credentials import Security
from app.services.EmailService import EmailService
from app.routers.middleware.SecurityMiddleware import SecurityMiddleware

from mangum import Mangum

# Main OverstocksAPI application
app = FastAPI()

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the scheduler
scheduler = AsyncIOScheduler()

# Function to schedule the async function with asyncio
async def schedule_mass_sync():
    try:
        await asyncio.gather(
            # Put the function that will be asynced here
        )
    except Exception as e:
        print(f"An error occurred during sync: {e}")

# This wrapper function will call the async function correctly
async def sync_job():
    await schedule_mass_sync()

# Schedule the job
trigger = CronTrigger(minute='*/30')  # Run every 30 minutes
scheduler.add_job(sync_job, trigger, misfire_grace_time=600)

asgi_handler = Mangum(app)

def lambda_handler(event, context):
    if "source" in event and event["source"] == "aws.scheduler":
        loop = asyncio.get_event_loop()
        # Use the loop to run the async sync task
        loop.run_until_complete(schedule_mass_sync())
        return {
            "statusCode": 200,
            "body": "Sync job completed successfully."
        }
    else:
        # For API Gateway events, return using Mangum
        return asgi_handler(event, context)

# Exception handler for 404
@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"status": 404, "message": "Oops! The resource you are looking for was not found."},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Global handler for HTTP exceptions (e.g., 400, 404, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    subject = f"HTTP Error - Status Code: {exc.status_code}"
    body = f"An HTTP error occurred:\n\nStatus: {exc.status_code}\nDetail: {exc.detail}\n"
    recipient_email = Env.admin_email
    # Send Email to the administrator
    await EmailService.send_error_email(subject, body, recipient_email)

    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "detail": exc.detail}
    )

# Global handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    subject = "Validation Error in OverstocksAPI - Status Code: 422"
    body = f"Validation Error:\n\nErrors: {exc.errors()}\nBody: {exc.body}\n"
    recipient_email = Env.admin_email
    # Send Email to the administrator
    await EmailService.send_error_email(subject, body, recipient_email)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": status.HTTP_422_UNPROCESSABLE_ENTITY, "detail": exc.errors()}
    )

# Catch-all handler for unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    subject = f"Unhandled Error in OverstocksAPI - {type(exc).__name__}"
    body = f"An unhandled error occurred:\n\nException Type: {type(exc).__name__}\nDetail: {str(exc)}\n"
    recipient_email = Env.admin_email
    # Send Email to the administrator
    await EmailService.send_error_email(subject, body, recipient_email)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "detail": "An internal server error occurred"}
    )

app.include_router(System.router)
app.add_middleware(GZipMiddleware)

overstock_api = FastAPI()
overstock_api.include_router(Overstocks.router)
overstock_api.add_middleware(
    SecurityMiddleware,
    expected_clientId=Security.clientId,
    expected_clientSecret=Security.clientSecret
)
overstock_api.add_middleware(GZipMiddleware)

app.mount('/overstock', overstock_api)

# Local server setup for testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)