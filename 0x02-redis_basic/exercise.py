#!/usr/bin/env python3

"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union


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
