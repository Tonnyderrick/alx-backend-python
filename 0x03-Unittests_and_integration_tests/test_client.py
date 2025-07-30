#!/usr/bin/env python3
"""Unittests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
from client import GithubOrgClient


@parameterized_class([
    {
        "org_payload": {"repos_url": "https://api.github.com/orgs/google/repos"},
        "repos_payload": [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}}
        ],
        "expected_repos": ["repo1", "repo2", "repo3"],
        "apache2_repos": ["repo1", "repo3"]
    }
])
class TestIntegrationGithubOrgClient_0(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch get_json before tests"""
        cls.get_patcher = patch('client.get_json')
        cls.mock_get_json = cls.get_patcher.start()

        # Mock responses based on call order
        cls.mock_get_json.side_effect = [
            cls.org_payload,        # First call to get_json -> org
            cls.repos_payload       # Second call -> list of repos
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filtering repos by license"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        apache_repos = [
            repo for repo in self.repos_payload
            if client.has_license(repo, "apache-2.0")
        ]
        expected = [repo["name"] for repo in apache_repos]
        self.assertEqual(expected, self.apache2_repos)
