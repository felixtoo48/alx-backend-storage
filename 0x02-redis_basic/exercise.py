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
