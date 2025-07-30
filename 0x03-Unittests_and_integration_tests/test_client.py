#!/usr/bin/env python3
"""Integration test module for GithubOrgClient.public_repos"""

import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class-level mocks for requests.get"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        # Configure side_effect to return proper mock responses in order
        mock_get.side_effect = [
            MagicMock(json=MagicMock(return_value=cls.org_payload)),
            MagicMock(json=MagicMock(return_value=cls.repos_payload)),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop class-level patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected result"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by license correctly"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
