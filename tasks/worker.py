"""
RQ worker entrypoint.

Run locally:
  set REDIS_URL=redis://localhost:6379/0
  python tasks/worker.py

On Render/production, run as a separate worker service using the same codebase.
"""

import os
from redis import Redis
from rq import Worker, Queue, Connection

from tasks.queue import get_redis_url

listen = ["default"]

def main():
    redis_url = get_redis_url()
    if not redis_url:
        raise SystemExit("REDIS_URL not set; cannot start worker.")

    conn = Redis.from_url(redis_url)
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=False)

if __name__ == "__main__":
    main()

