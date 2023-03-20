import requests

from autopr.models.repo import RepoPullRequest


class PullRequestService:
    def publish(self, pr: RepoPullRequest):
        raise NotImplementedError

    def update(self, pr: RepoPullRequest):
        raise NotImplementedError


class GithubPullRequestService(PullRequestService):
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

    def publish(self, pr: RepoPullRequest):
        existing_pr = self._find_existing_pr()
        if existing_pr:
            self.update(pr)
        else:
            self._create_pr(pr)

    def _create_pr(self, pr: RepoPullRequest):
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
            print('Pull request created successfully')
            print(response.json())
        else:
            print('Failed to create pull request')
            print(response.text)

    def update(self, pr: RepoPullRequest):
        existing_pr = self._find_existing_pr()
        if not existing_pr:
            print("No existing pull request found to update")
            return

        url = f'https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{existing_pr["number"]}'
        headers = self._get_headers()
        data = {
            'title': pr.title,
            'body': pr.body,
        }
        response = requests.patch(url, json=data, headers=headers)

        if response.status_code == 200:
            print('Pull request updated successfully')
            print(response.json())
        else:
            print('Failed to update pull request')
            print(response.text)

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
            print('Failed to get pull requests')
            print(response.text)

        return None
