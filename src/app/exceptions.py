import logging
from typing import cast

from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse

logger = logging.getLogger("myapp")


# Handle expected HTTP errors
async def http_exception_handler(request: Request, exc: Exception) -> Response:
    exc = cast(HTTPException, exc)
    logger.warning(f"HTTP error: {exc.detail} on {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# Handle unexpected errors
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled error: {exc} on {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
