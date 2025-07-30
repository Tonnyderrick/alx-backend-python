#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        """Test that memoization caches the result of a method call"""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mocked_method:
            obj = TestClass()

            # Call the memoized method twice
            result1 = obj.a_property()
            result2 = obj.a_property()

            # Assert result is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert a_method is only called once due to memoization
            mocked_method.assert_called_once()
