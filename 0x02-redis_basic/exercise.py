#!/usr/bin/env python3

"""
Class Cache, decorators and methods
"""
import redis
import uuid
from typing import Any, Union, Callable, Optional
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

def call_history(method: Callable) -> Callable:
    """
    call history decorator
    """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """
        Wrapper method that also implements: to store
        the history of inputs and outputs for a particular function
        """

        # append ":inputs" and ":outputs" to create input and output list keys
        input_keys = method.__qualname__ + ":inputs"
        output_keys = method.__qualname__ + ":outputs"

        # store the input args in Redis
        self._redis.rpush(input_keys, str(args))

        # Store output in the "...:outputs" list, then return the output
        result = method(self, *args, **kwds)
        self._redis.rpush(output_keys, str(result))

        return result
    return wrapper

def replay(method: Callable[..., Any]) -> None:
    """
    Displays the history of calls of a particular function
    """
    inputs = method.__self__._redis.lrange(method.__qualname__ + ":inputs", 0, -1)
    outputs = method.__self__._redis.lrange(method.__qualname__ + ":outputs", 0, -1)

    print(f'{method.__qualname__} was called \
{method.__self__._redis.get(method.__qualname__).decode("utf-8")} times:')
    for In , Out in zip(inputs, outputs):
        print(f'{method.__qualname__}(*{In.decode("utf-8")}) -> {Out.decode("utf-8")}')

class Cache(object):
    """
    class Cache to be used to write strings to Redis
    """
    def __init__(self) -> None:
        """ Init method """
        self._redis = redis.Redis()
        self._redis.flushdb()  # Flush database to clear old entries

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store method that returns a string"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    @count_calls
    @call_history
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
    @call_history
    def get_str(self, key: str) -> str:
        """Retrieves value of key from Redis and converts it to a str"""
        value = self.get(key)
        if value is None:
            return None
        else:
            return value.decode('utf-8')

    @count_calls
    @call_history
    def get_int(self, key: str) -> int:
        """Retrieves value of key from Redis and converts it to an int"""
        value = self.get(key)
        if value is not None:
            return int(value)
        return None
