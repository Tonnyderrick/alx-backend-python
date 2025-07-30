# utils.py

import requests
from functools import wraps

def access_nested_map(nested_map, path):
    """Access a nested map using a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url):
    """Get JSON content from a URL."""
    response = requests.get(url)
    return response.json()

def memoize(method):
    """Memoization decorator to cache method results."""
    attr_name = f"_memoized_{method.__name__}"

    @wraps(method)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)
    return wrapper
