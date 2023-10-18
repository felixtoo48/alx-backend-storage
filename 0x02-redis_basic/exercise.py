#!/usr/bin/env python3
""" redis-py exercise """
import redis
import uuid
from typing import Union


class Cache():
    def __init__(self, host='localhost', port=6379,
                 db=0,):
        """ initializing the class method to store
        an instance of the redis client"""
        self._redis = redis.Redis(host=host, port=port, db=db)
        # clear database
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ method that takes in data argument and returns a string """
        # Generate a random key using uuid
        random_key = str(uuid.uuid4())
        # Store the input data in Redis using the random key
        self._redis.set(random_key, data)
        # Return the random key as a string
        return random_key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
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
