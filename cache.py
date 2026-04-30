import os
import time
from functools import wraps
from flask import request, make_response

def add_cache_control(max_age=3600, public=True):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            cache_control = 'public' if public else 'private'
            response.headers['Cache-Control'] = f'{cache_control}, max-age={max_age}'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'SAMEORIGIN'
            return response
        return decorated_function
    return decorator

class SimpleCache:
    def __init__(self, timeout=300):
        self.cache = {}
        self.timeout = timeout
    
    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry['time'] < self.timeout:
                return entry['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        self.cache[key] = {'value': value, 'time': time.time()}
    
    def clear(self):
        self.cache.clear()

cache = SimpleCache(timeout=600)

def cached(timeout=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = request.path + str(request.args)
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            result = f(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        return decorated_function
    return decorator
