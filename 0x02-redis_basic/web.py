import requests
import redis
import time
from functools import wraps

# Initialize the Redis client
r = redis.Redis()

def cache_with_expiration(expiration: int):
    """
    Decorator to cache the result of the function in Redis with an expiration time.
    Also tracks how many times a particular URL was accessed.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url: str):
            cache_key = f"cache:{url}"
            count_key = f"count:{url}"

            # Check if the URL content is already cached
            cached_result = r.get(cache_key)
            if cached_result:
                print(f"Cache hit for {url}")
                return cached_result.decode('utf-8')

            # If not cached, fetch the content
            print(f"Cache miss for {url}. Fetching...")
            result = func(url)

            # Store the result in cache with an expiration time
            r.setex(cache_key, expiration, result)

            # Increment the access count
            r.incr(count_key)

            return result

        return wrapper
    return decorator

@cache_with_expiration(10)
def get_page(url: str) -> str:
    """
    Fetch the content of a URL and cache the result with an expiration time.
    Track the number of times the URL is accessed.
    """
    response = requests.get(url)
    return response.text
