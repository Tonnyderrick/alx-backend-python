#!/usr/bin/env python3
""" GitHub Org Client """

from typing import Dict
import requests


def get_json(url: str) -> Dict:
    """Return JSON content from the given URL"""
    return requests.get(url).json()


class GithubOrgClient:
    """GitHub Org Client"""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        self._org_name = org_name

    @property
    def org(self) -> Dict:
        """Fetch organization data"""
        return get_json(self.ORG_URL.format(self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Extract and return public repositories URL"""
        return self.org.get("repos_url")
