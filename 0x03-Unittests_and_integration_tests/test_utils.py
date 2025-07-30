#!/usr/bin/env python3
"""
Unit test module for utils.memoize function.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test class for memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""

        class TestClass:
            """A class with a method and a memoized property."""

            def a_method(self):
                """Returns a fixed integer."""
                return 42

            @memoize
            def a_property(self):
                """Calls a_method and returns its result."""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mocked_method:
            mocked_method.return_value = 42
            obj = TestClass()

            result1 = obj.a_property()
            result2 = obj.a_property()

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mocked_method.assert_called_once()
