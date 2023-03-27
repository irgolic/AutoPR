import requests

from autopr.models.rail_objects import PullRequestDescription

import structlog
log = structlog.get_logger()


class PublishService:
    def publish(self, pr: PullRequestDescription):
        raise NotImplementedError

    def update(self, pr: PullRequestDescription):
        raise NotImplementedError


class GithubPublishService(PublishService):
    def __init__(self, token: str, owner: str, repo_name: str, head_branch: str, base_branch: str):
        self.token = token
        self.owner = owner
        self.repo = repo_name
        self.head_branch = head_branch
        self.base_branch = base_branch

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
        }

    def publish(self, pr: PullRequestDescription):
        existing_pr = self._find_existing_pr()
        if existing_pr:
            self.update(pr)
        else:
            self._create_pr(pr)

    def _create_pr(self, pr: PullRequestDescription):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/pulls'
        headers = self._get_headers()
        data = {
            'head': self.head_branch,
            'base': self.base_branch,
            'title': pr.title,
            'body': pr.body,
        }
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 201:
            log.debug('Pull request created successfully', response=response.json())
        else:
            log.debug('Failed to create pull request', response_text=response.text)

    def update(self, pr: PullRequestDescription):
        existing_pr = self._find_existing_pr()
        if not existing_pr:
            log.debug("No existing pull request found to update")
            return

        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{existing_pr["number"]}'
        headers = self._get_headers()
        data = {
            'title': pr.title,
            'body': pr.body,
        }
        response = requests.patch(url, json=data, headers=headers)

        if response.status_code == 200:
            log.debug('Pull request updated successfully', response=response.json())
        else:
            log.debug('Failed to update pull request', response_text=response.text)

    def _find_existing_pr(self):
        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/pulls'
        headers = self._get_headers()
        params = {'state': 'open', 'head': f'{self.owner}:{self.head_branch}', 'base': self.base_branch}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            prs = response.json()
            if prs:
                return prs[0]  # Return the first pull request found
        else:
            log.debug('Failed to get pull requests', response_text=response.text)

        return None
