#!/usr/bin/env python3
""" mplementing an expiring web cache and tracker"""
import requests
import redis
from functools import wraps


# Initialize a Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# Decorator for caching and tracking
def cache_and_track(url):
    """caching and tracking method"""
    def decorator(func):
        """decortor"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            """ wrapper"""
            # Count the number of times the URL was accessed
            count_key = f"count:{url}"
            visit_count = redis_client.get(count_key)
            if visit_count is None:
                visit_count = 1
            else:
                visit_count = int(visit_count) + 1
            redis_client.setex(count_key, 10, visit_count)

            # Check if the page is already cached
            cached_result = redis_client.get(url)
            if cached_result is not None:
                return cached_result.decode("utf-8")

            # If not cached, fetch the page content
            page_content = func(*args, **kwargs)

            # Cache the result with a 10-second expiration time
            redis_client.setex(url, 10, page_content)

            return page_content

        return wrapper

    return decorator

# Define the get_page function
@cache_and_track("http://slowwly.robertomurray.co.uk")
def get_page(url: str) -> str:
    """ defining get page function"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""
