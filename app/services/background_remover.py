from rembg import new_session, remove

SUPPORTED_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

_session = None


def _get_session():
    global _session
    if _session is None:
        _session = new_session("u2netp")
    return _session


class BackgroundRemovalError(Exception):
    pass


def remove_background(data: bytes) -> bytes:
    if not data:
        raise BackgroundRemovalError("Uploaded file is empty.")
    try:
        return remove(data, session=_get_session())
    except Exception as exc:
        raise BackgroundRemovalError(f"Background removal failed: {exc}") from exc
