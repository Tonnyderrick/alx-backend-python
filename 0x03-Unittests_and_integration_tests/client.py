#!/usr/bin/env python3
"""Github Org Client"""
from typing import List
from functools import lru_cache
import requests


def get_json(url: str) -> dict:
    """Return JSON content from a REST API endpoint."""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Github Organization Client"""

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """Initialize with organization name"""
        self._org_name = org_name

    @property
    @lru_cache()
    def org(self) -> dict:
        """Cached organization data"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Return the public repos URL"""
        return self.org.get("repos_url")

    def public_repos(self) -> List[str]:
        """Get list of public repository names"""
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

    @staticmethod
    def has_license(repo: dict, license_key: str) -> bool:
        """Check if repo has the given license"""
        return repo.get("license", {}).get("key") == license_key
