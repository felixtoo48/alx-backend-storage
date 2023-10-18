#!/usr/bin/env python3
""" redis-py exercise """
import redis
import sys
import uuid
from typing import Union, Callable, Optional, list
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count number of calls made to a method"""
    key = method.__qualname__

    @wraps(method)
    def counter(self, *args, **kwargs):
        """decorator method"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return counter


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def history_wrapper(self, *args, **kwargs):
        """set list keys to a wrapped function"""
        in_list_key = method.__qualname__ + ":inputs"
        out_list_key = method.__qualname__ + ":outputs"
        self._redis.rpush(in_list_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(out_list_key, str(output))
        return output
    return history_wrapper


def replay(method: Callable) -> None:
    """function displays the history of calls of a particular function"""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"
    server = method.__self__._redis
    count = server.get(key).decode("utf-8")
    print(f"{key} was called {count} times:")
    input_list = server.lrange(inputs, 0, -1)
    output_list = server.lrange(outputs, 0, -1)
    zipped = list(zip(input_list, output_list))
    for k, v in zipped:
        attr, result = k.decode("utf-8"), k.decode("utf-8")
        print(f"{key}(*{attr}) -> {result}")


class Cache():
    def __init__(self, host='localhost', port=6379,
                 db=0,):
        """ initializing the class method to store
        an instance of the redis client"""
        self._redis = redis.Redis(host=host, port=port, db=db)
        # clear database
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ method that takes in data argument and returns a string """
        # Generate a random key using uuid
        random_key = str(uuid.uuid4())
        # Store the input data in Redis using the random key
        self._redis.set(random_key, data)
        # Return the random key as a string
        return random_key

    def get(self, key: str, fn: Callable = None) ->\
            Union[str, bytes, int, float, None]:
        """ method that takes key argument and an optinal callable argument fn
        and return converted data back to desired format"""
        # Get the value from Redis
        value = self._redis.get(key)

        if value is not None:
            # If a conversion function is provided, apply it
            if fn is not None:
                return fn(value)

            # If no conversion function is provided, return the value as is
            return value

        return None

    def get_str(self, key: str) -> Union[str, bytes, None]:
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)
