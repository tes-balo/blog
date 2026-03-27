import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response


# ----------------------------
# 2. Logging Middleware
# ----------------------------
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time: float = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        logging.info(
            f"{request.method} {request.url.path} completed_in={process_time:.2f}ms status_code={response.status_code}"
        )
        return response
