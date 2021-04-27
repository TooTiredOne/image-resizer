import os

from redis import Redis
from rq import Queue

REDIS_URL = os.getenv('REDIS_URL', default='redis://redis:6379/0')

redis_conn = Redis.from_url(url=REDIS_URL)
queue = Queue(connection=redis_conn)
