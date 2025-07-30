#!/usr/bin/env python3
""" GitHub Org Client module """

from typing import Dict
import requests


def get_json(url: str) -> Dict:
    """Fetch JSON content from a URL"""
    return requests.get(url).json()


class GithubOrgClient:
    """GitHub organization client"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        """Initialize with org name"""
        self._org_name = org_name

    @property
    def org(self) -> Dict:
        """Fetch the organization data"""
        url = self.ORG_URL.format(self._org_name)
        return get_json(url)

    @property
    def _public_repos_url(self) -> str:
        """Return the public repos URL from org"""
        return self.org.get("repos_url")
