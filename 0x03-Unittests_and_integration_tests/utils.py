#!/usr/bin/env python3
"""Utils module with memoize"""

def memoize(method):
    """Decorator to cache method output in instance attributes"""
    attr_name = "_{}".format(method.__name__)

    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self))
        return getattr(self, attr_name)

    return wrapper
