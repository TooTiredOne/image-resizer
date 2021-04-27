import os

REDIS_URL = os.getenv('REDIS_URL', default='redis://redis:6379/0')
