#!/usr/bin/env python3
"""
Unit test module for utils.memoize function.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test class for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""

        class TestClass:
            """Test class with a method and a memoized property."""

            def a_method(self):
                """Return a constant value."""
                return 42

            @memoize
            def a_property(self):
                """Return value from a_method."""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mocked_method:
            mocked_method.return_value = 42
            obj = TestClass()

            first = obj.a_property()
            second = obj.a_property()

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mocked_method.assert_called_once()
