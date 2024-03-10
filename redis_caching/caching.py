import json
from functools import wraps
from time import time as current_timestamp

import redis


class RedisCaching:
    """
    RedisCaching provides caching functionalities using Redis for storing and retrieving cached values.
    """
    
    def __init__(self, log: bool = True, **kwargs):
        self.log = log

        self._redis_client = redis.Redis(**kwargs)

        self._log("The logging is currently on. If you wish to turn it off, simply include log=False as an argument in the __init__ function.")

        self._pre_ping()

    def _pre_ping(self) -> None:
        self._log("A ping was sent to the Redis server.")

        self._redis_client.ping()

        self._log("The Redis server received a ping.")

    def _log(self, message: str) -> None:
        if self.log is True:
            print(f'[Redis Caching] * {message}')

    def get_cache(self, cache_key: str):
        if cache_key is None:
            raise Exception('Cache key cannot be None')

        cache_value = self._redis_client.get(cache_key)

        if cache_value is None:
            self._log(f'No cached value for "{cache_key}" key.')

            return None
        
        cache_value = json.loads(cache_value)
        
        expires_in = cache_value.get('expires_in')

        if expires_in is not None and (expires_in + cache_value.get('timestamp')) < current_timestamp():
            self._log(f'Expired cache value for "{cache_key}" key.')

            return None

        self._log(f'Got cached value for "{cache_key}" key.')

        return cache_value.get('value')
    
    def set_cache(self, cache_key: str, cache_value, expires_in: int = None) -> None:
        if expires_in is not None and not isinstance(expires_in, int):
            raise Exception("expires_in must be an integer")
    
        cache_value = {
            'value': cache_value,
            'timestamp': current_timestamp(),
            'expires_in': expires_in
        }

        cache_value = json.dumps(cache_value)

        self._redis_client.set(cache_key, cache_value)

        self._log(f'Set cached value for "{cache_key}" key.')

    def make_cache_expired(self, cache_key: str) -> None:
        if self._redis_client.get(cache_key) is None:
            return

        self._log(f'Made cache expired for "{cache_key}" key.')

        del self._redis_client[cache_key]

    def cached_result(caching_instance, is_class_function: bool, cache_key: str = None, cache_key_getter=None, expires_in: int = None):
        def decorator(f):
            @wraps(f)
            def wrapped(self=None, *args, **kwargs):
                _cache_key = cache_key

                if _cache_key is None and cache_key_getter is not None:
                    if not is_class_function:
                        _cache_key = cache_key_getter()
                    else:
                        _cache_key = cache_key_getter(self)
                    
                elif _cache_key is not None and cache_key_getter is not None:
                    raise Exception("You cannot use cache_key and cache_key_getter at the same time.")

                cached_value = caching_instance.get_cache(
                    cache_key=_cache_key
                )

                if cached_value is not None:
                    return cached_value

                if not is_class_function:
                    value = f(*args, **kwargs)
                else:
                    value = f(self, *args, **kwargs)

                caching_instance.set_cache(
                    cache_key=_cache_key,
                    cache_value=value,
                    expires_in=expires_in
                )

                return value
            return wrapped
        return decorator