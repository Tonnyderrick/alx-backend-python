# test_utils.py
#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import get_json


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        # Patch 'requests.get' from the utils module
        with patch('utils.requests.get') as mock_get:
            # Create a Mock object with a `.json()` method returning test_payload
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function
            result = get_json(test_url)

            # Ensure requests.get was called once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Check that the returned result matches the mock payload
            self.assertEqual(result, test_payload)
