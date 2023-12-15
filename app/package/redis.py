"""redis.py"""
import os
from typing import Tuple

import redis

from .enums import RedisStatus


def redis_connect(host_url: str, local: bool, password:str, port:int) -> Tuple[RedisStatus, redis.client.Redis]:
    """Attempt to connect to `host_url` depends on `local` if it sets to `true` it will connect to `cloud` with `password` and return a Redis client instance if successful."""
    return _connect(host_url) if local is True else _connect_cloud(host_url, password, port)
        # if os.environ.get("CACHE_ENV") != "TEST" else _connect_fake()


def _connect(host_url: str) -> Tuple[RedisStatus, redis.client.Redis]:  # pragma: no cover
    try:
        redis_client = redis.from_url(host_url)
        if redis_client.ping():
            return RedisStatus.CONNECTED, redis_client
        return RedisStatus.CONN_ERROR, None
    except redis.AuthenticationError:
        return RedisStatus.AUTH_ERROR, None
    except redis.ConnectionError:
        return RedisStatus.CONN_ERROR, None

def _connect_cloud(host_url: str, password:str, port:int):
    try:
        redis_client = redis.Redis(host = host_url, password = password, port = port)
        if redis_client.ping():
            return RedisStatus.CONNECTED, redis_client
        return RedisStatus.CONN_ERROR, None
    except redis.AuthenticationError:
        return RedisStatus.AUTH_ERROR, None
    except redis.ConnectionError:
        return RedisStatus.CONN_ERROR, None
