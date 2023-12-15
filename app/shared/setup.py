from fastapi import Response, Request
from sqlalchemy.orm import Session

from app.package import FastApiRedisCache
from app.shared import settings
from app.shared.logger import logger_system


class RedisCacheSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisCacheSingleton, cls).__new__(cls)
            cls._instance.initialize_redis_cache()
        return cls._instance

    def initialize_redis_cache(self):
        self.redis_cache = FastApiRedisCache(
            prefix = "myapi-cache" ,
            response_header = "X-MyAPI-Cache" ,
            ignore_arg_types = [Request , Response , Session] ,
            logger_system = logger_system ,
            host_url = settings.REDIS_HOSTNAME ,
            port = settings.REDIS_PORT ,
            password = settings.REDIS_PASSWORD
        )

    def get_redis( self ):
        return self.redis_cache.redis
