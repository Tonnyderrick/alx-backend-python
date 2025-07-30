#!/usr/bin/env python3
"""GithubOrgClient module"""

import requests
from typing import List
from functools import lru_cache


def get_json(url: str) -> dict:
    """Fetch JSON from a URL"""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """GitHub Organization Client"""
    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str):
        self._org_name = org_name

    @property
    @lru_cache()
    def org(self) -> dict:
        """Get organization info"""
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Get the repos URL"""
        return self.org.get("repos_url")

    def public_repos(self) -> List[str]:
        """Return list of public repo names"""
        repos = get_json(self._public_repos_url)
        return [repo["name"] for repo in repos]

    def has_license(self, repo: dict, license_key: str) -> bool:
        """Check if repo has a specific license"""
        return repo.get("license", {}).get("key") == license_key
