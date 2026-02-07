from redis import Redis
from rq import Connection, Queue, Worker

from app.core.config import settings


def main() -> None:
    redis_conn = Redis.from_url(settings.redis_url)
    with Connection(redis_conn):
        worker = Worker([Queue("webhooks")])
        worker.work(with_scheduler=True)


if __name__ == "__main__":
    main()
