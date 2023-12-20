#!/usr/bin/env python3

"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count_calls decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Wrapper method that also implements how many times
        the methods of Cache class are called
        """
        key = method.__qualname__
        self._redis.incr(key, 1)

        return method(self, *args, **kwds)
    return wrapper

class Cache(object):
    """
    class Cache to be used to write strings to Redis
    """
    def __init__(self) -> None:
        """ Init method """
        self._redis = redis.Redis()
        self._redis.flushdb()  # Flush database to clear old entries

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store method that returns a string"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    @count_calls
    def get(self, key: str, fn: Optional[Callable] = None):
        """
        get method that take a key string argument,
        and an optional Callable argument named fn
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        else:
            return value

    @count_calls
    def get_str(self, key: str) -> str:
        """Retrieves value of key from Redis and converts it to a str"""
        value = self.get(key)
        if value is None:
            return None
        else:
            return value.decode('utf-8')

    @count_calls
    def get_int(self, key: str) -> int:
        """Retrieves value of key from Redis and converts it to an int"""
        value = self.get(key)
        if value is not None:
            return int(value)
        return None
