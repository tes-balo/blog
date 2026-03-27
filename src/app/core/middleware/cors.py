from typing import Any

from starlette.middleware.cors import CORSMiddleware

__all__ = ["CORSMiddleware", "cors_config"]

cors_config: dict[str, Any] = {
    "allow_origins": ["https://myfrontend.com"],
    "allow_methods": ["*"],
    "allow_headers": ["*"],
    "allow_credentials": True,
}
