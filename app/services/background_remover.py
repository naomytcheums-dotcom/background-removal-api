from rembg import new_session, remove

_SESSION = new_session("u2netp")

SUPPORTED_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}


class BackgroundRemovalError(Exception):
    pass


def remove_background(data: bytes) -> bytes:
    if not data:
        raise BackgroundRemovalError("Uploaded file is empty.")
    try:
        return remove(data, session=_SESSION)
    except Exception as exc:
        raise BackgroundRemovalError(f"Background removal failed: {exc}") from exc
