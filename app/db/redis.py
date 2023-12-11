from app.shared import redis


async def rate_limit_get(identifier: str) -> tuple[int, int]:
    key = 'rate_limit:' + identifier

    value = await redis.get(key)
    if value is None:
        return 0, 0

    expire = await redis.ttl(key)
    return int(value), expire


async def rate_limit_set(identifier: str, period: int):
    key = 'rate_limit:' + identifier

    if await redis.exists(key):
        await redis.incr(key, 1)
    else:
        await redis.setex(key, 1, period)


__all__ = [
    'rate_limit_get',
    'rate_limit_set',
]
