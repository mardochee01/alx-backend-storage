#!/usr/bin/env python3
"""Writing strings to Redis"""


import redis
from typing import Union, Callable
from uuid import uuid4
from functools import wraps


def call_history(method: Callable) -> Callable:
    """Calls a method history"""
    qualified_name = method.__qualname__
    inp_key = qualified_name + ":inputs"
    outp_key = qualified_name + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Stores the data in a redis db"""
        self._redis.rpush(inp_key, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outp_key, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """counts how many times methods of the Cache"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """increments the key"""
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def replay(method: Callable) -> None:
    """displays the history of calls"""
    redis = method.__self__._redis
    qualified_name = method.__qualname__
    num_of_calls = redis.get(qualified_name).decode("utf-8")
    print("{} was called {} times:".format(qualified_name, num_of_calls))
    inp_key = qualified_name + ":inputs"
    outp_key = qualified_name + ":outputs"
    inp_list = redis.lrange(inp_key, 0, -1)
    outp_list = redis.lrange(outp_key, 0, -1)
    r_zipped = list(zip(inp_list, outp_list))
    for key, value in r_zipped:
        key = key.decode("utf-8")
        value = value.decode("utf-8")
        print("{}(*{}) -> {}".format(qualified_name, key, value))


class Cache:
    """defines method, store instance"""

    def __init__(self):
        """store an instance of
        the Redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """takes data arg, return string"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """convert data for desired format"""
        call = self._redis.get(key)
        if fn is not None:
            return fn(call)
        return call

    def get_str(self, key: str) -> str:
        """Cache.get with the correct conversion"""
        getstr = self._redis.get(key)
        return getstr.decode('UTF-8')

    def get_int(self, key: str) -> int:
        """Cache.get with the correct conversion"""
        getint = self._redis.get(key)
        try:
            getint = int(getint.decode('UTF-8'))
        except Exception:
            getint = 0
        return getint
