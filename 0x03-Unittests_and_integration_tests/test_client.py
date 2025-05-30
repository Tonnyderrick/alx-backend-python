import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient  # Adjust import if class is elsewhere

class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient.org"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value and get_json called correctly."""
        test_response = {"login": org_name, "id": 123}
        mock_get_json.return_value = test_response
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_response)

if __name__ == '__main__':
    unittest.main()