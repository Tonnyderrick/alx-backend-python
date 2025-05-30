#!/usr/bin/env python3
"""Unit tests for GithubOrgClient.org method."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        # Define expected payload based on input org_name
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        # Instantiate client and call .org
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)

        # Verify get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == '__main__':
    unittest.main()
