#!/usr/bin/env python3
"""
Integration test module for GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {"org_payload": TEST_PAYLOAD[0][0],
     "repos_payload": TEST_PAYLOAD[0][1],
     "expected_repos": TEST_PAYLOAD[0][2],
     "apache2_repos": TEST_PAYLOAD[0][3]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Integration test for GithubOrgClient.public_repos """

    @classmethod
    def setUpClass(cls):
        """ Patch requests.get and set up payloads """
        cls.get_patcher = patch('requests.get')

        # Start the patcher and store the mock object
        mock_get = cls.get_patcher.start()

        # Side effects in order: org_payload first, then repos_payload
        mock_get.side_effect = [
            unittest.mock.Mock(**{"json.return_value": cls.org_payload}),
            unittest.mock.Mock(**{"json.return_value": cls.repos_payload})
        ]

    @classmethod
    def tearDownClass(cls):
        """ Stop patching requests.get """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ Test that public_repos returns expected repos """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """ Test that public_repos filters by license """
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
