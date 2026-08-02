import onnxruntime as ort
from rembg import new_session, remove

SUPPORTED_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}

_session = None


def _get_session():
    global _session
    if _session is None:
        sess_opts = ort.SessionOptions()
        sess_opts.intra_op_num_threads = 1
        sess_opts.inter_op_num_threads = 1
        sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_BASIC
        _session = new_session(
            "u2netp",
            sess_opts=sess_opts,
            providers=["CPUExecutionProvider"],
        )
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
