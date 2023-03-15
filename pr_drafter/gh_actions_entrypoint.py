import os

from pr_drafter.main import main

repo_path = os.environ['GITHUB_WORKSPACE']

token = os.environ['INPUT_TOKEN']
base_branch = os.environ['INPUT_BASE_BRANCH']
issue_number = int(os.environ['INPUT_ISSUE_NUMBER'])
issue_title = os.environ['INPUT_ISSUE_TITLE']
issue_body = os.environ['INPUT_ISSUE_BODY']

main(
    repo_path=repo_path,
    base_branch_name=base_branch,
    issue_number=issue_number,
    issue_title=issue_title,
    issue_body=issue_body,
)
