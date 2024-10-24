from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from fastapi import HTTPException, status, Response
import json

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, expected_clientId: str, expected_clientSecret: str):
        super().__init__(app)
        self.expected_clientId = expected_clientId
        self.expected_clientSecret = expected_clientSecret

    async def dispatch(self, request: Request, call_next):
        clientId = request.headers.get("client_id")
        clientSecret = request.headers.get("client_secret")

        # Check if credentials are missing or don't match
        if (not clientId or clientId != self.expected_clientId) or (not clientSecret or clientSecret != self.expected_clientSecret):
            # Customize the error response
            return Response(
                content=json.dumps({
                    "status": 401,
                    "detail": "Invalid or missing credentials"
                }),
                status_code=status.HTTP_401_UNAUTHORIZED,
                media_type="application/json"
            )

        # Proceed if credentials are valid
        response = await call_next(request)
        return response