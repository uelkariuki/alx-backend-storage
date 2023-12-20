#!/usr/bin/env python3

"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache(object):
    """
    class Cache to be used to write strings to Redis
    """
    def __init__(self) -> None:
        """ Init method """
        self._redis = redis.Redis()
        self._redis.flushdb()  # Flush database to clear old entries

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store method that returns a string"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable]):
        """
        get method that take a key string argument,
        and an optional Callable argument named fn
        """
        value = self._redis.get(key)
        if value is None:
            return None
        elif fn is not None:
            return fn(value)
        else:
            return value

    def get_str(self, key: str) -> str:
        """Retrieves value of key from Redis and converts it to a str"""
        value = self.get(key)
        if value is None:
            return None
        else:
            return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """Retrieves value of key from Redis and converts it to an int"""
        value = self.get(key)
        if value:
            return int(value)
        return None
