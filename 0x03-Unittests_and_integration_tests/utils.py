# utils.py

import requests

def access_nested_map(nested_map, path):
    """Access a nested map using a sequence of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map

def get_json(url):
    """Get JSON content from a URL."""
    response = requests.get(url)
    return response.json()
