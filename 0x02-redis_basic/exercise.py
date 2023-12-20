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

def replay(method):
    """
    Displays the history of calls of a particular function
    """
    history = []

    def wrapper(self, *args, **kwargs):
        """
        Wrapper method
        """
        result = method(self, *args, **kwargs)
        history.append((args, kwargs, result))
        return result

    def print_history_template():
        """ Template for printing the history output"""
        print(f'{method.__qualname__} was called {len(history)} times:')
        for x, call in enumerate(history, 1):
            args, kwargs, result = call
            print(f'{method.__qualname__}{args} -> {result}')

    wrapper.print_history_template = print_history_template
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
    @call_history
    @replay
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store method that returns a string"""
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    @count_calls
    @call_history
    @replay
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
    @replay
    def get_str(self, key: str) -> str:
        """Retrieves value of key from Redis and converts it to a str"""
        value = self.get(key)
        if value is None:
            return None
        else:
            return value.decode('utf-8')

    @count_calls
    @call_history
    @replay
    def get_int(self, key: str) -> int:
        """Retrieves value of key from Redis and converts it to an int"""
        value = self.get(key)
        if value is not None:
            return int(value)
        return None
