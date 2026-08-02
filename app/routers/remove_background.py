from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import Response

from app.auth import require_api_key
from app.services.background_remover import (
    SUPPORTED_TYPES,
    BackgroundRemovalError,
    remove_background,
)

router = APIRouter(prefix="/api", tags=["background-removal"])


@router.post("/remove-background", dependencies=[Depends(require_api_key)])
async def remove_background_endpoint(image: UploadFile) -> Response:
    if image.content_type not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type '{image.content_type}'. Use PNG, JPEG, or WEBP.",
        )
    data = await image.read()
    try:
        output = remove_background(data)
    except BackgroundRemovalError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return Response(content=output, media_type="image/png")


@router.get("/health")
async def health() -> dict:
    return {"status": "ok"}
