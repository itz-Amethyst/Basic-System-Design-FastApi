from functools import wraps
import time

from fastapi import HTTPException , status


# Todo: Make it better by storing user ip if it's exceeded in database and time
def rate_limited(max_calls:int , time_frame: int):
    """
    :param max_calls: Maximum number of cells or Requests Allowed in specified time_frame.
    :param time_frame: The time (in seconds) for applying limit.
    :return: Decorator Function.
    """

    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time.time()
            calls_in_time_frame = [call for call in calls if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                raise HTTPException(status_code = status.HTTP_429_TOO_MANY_REQUESTS, detail = "Rate limit exceeded.!")

            calls.append(now)
            return await func(*args, **kwargs)

        return wrapper

    return decorator
