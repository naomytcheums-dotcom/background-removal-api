from fastapi import Header, HTTPException

from app.config import settings


async def require_api_key(x_api_key: str | None = Header(None)) -> None:
    if not settings.api_access_key:
        return
    if x_api_key != settings.api_access_key:
        raise HTTPException(status_code=401, detail="Missing or invalid X-API-Key.")
