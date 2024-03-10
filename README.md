# Redis Caching

## Overwiew
Redis Caching is a Python library that provides caching functionalities using Redis for storing and retrieving cached values. This library aims to simplify caching operations and improve application performance by reducing database queries and computation time through caching.

## Installation
You can install Redis Caching via pip:

``` python
pip install redis-caching
```

## Features
- ***Dynamic Cache Key Generation***: Can generate cache keys dynamically based on input parameters or custom logic, enabling flexible caching strategies (cache_key_getter param).
- Redis Integration: Seamless integration with Redis for efficient storage and retrieval of cached values.
- Decorator-based Caching: Easily cache the results of functions and methods using decorator syntax, reducing boilerplate code.
- Automatic Cache Expiration: Set expiration times for cached values, ensuring data remains fresh and relevant.

## Usage
### Initialization
Initialize Redis Caching by passing the credentials (**kwargs)) to the `RedisCaching` constructor:

``` python
from redis_caching import RedisCaching

redis_caching = RedisCaching(
  host=host,
  port=6379,
  password=password,
  username=username
)
```

### Caching Decorators
Class Method Caching
You can cache the result of a class method using the cached_result decorator. Example:

``` python
class DynamicValues:
    def __init__(self, uuid: str) -> None:
        self.uuid = uuid

    @redis_caching.cached_result(
        cache_key_getter=lambda self: self.uuid + '-long_function', # Dynamic cache_key, for e.g you can access here the class object.
        expires_in=60,
        is_class_function=True
    )
    def long_function(self):
        # Your expensive computation here
```

Function Caching
Similarly, you can cache the result of a function using the cached_result decorator. Example:

```python
@redis_caching.cached_result(cache_key="long_function", is_class_function=False, expires_in=30) # cache_key_getter can be used aswell.
def long_function():
    # Your expensive computation here
```

### Cache Management
You can manually expire a cached value using the make_cache_expired method:

```python
def function_that_expires_the_cache():
    redis_caching.make_cache_expired('long_function')
```

### Example
```python
from time import sleep
from redis_caching import RedisCaching

redis_caching = RedisCaching(
  host=host,
  port=6379,
  password=password,
  username=username
)

@redis_caching.cached_result(cache_key="long_function", is_class_function=False, expires_in=30)
def long_function():
    sleep(5)

    return "Lemme cache this"

result = long_function()  # If the cached value is present, it will be returned; otherwise, the function will be executed.

```

### Logging
RedisCaching provides optional logging to track caching operations. Logging is enabled by default, but you can disable it by passing `log=False` during initialization.

### Contributing
If you have any suggestions, bug reports, or contributions, feel free to open an issue or create a pull request on GitHub.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
