import os

def get_redis_url() -> str | None:
    url = (os.environ.get("REDIS_URL") or "").strip()
    return url or None

def is_queue_enabled() -> bool:
    return get_redis_url() is not None

