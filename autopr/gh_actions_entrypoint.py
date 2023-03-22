import os

import structlog
log = structlog.get_logger()


if __name__ == '__main__':
    log.info("Starting gh_actions_entrypoint.py")

    repo_path = os.environ['GITHUB_WORKSPACE']

    github_token = os.environ['INPUT_GITHUB_TOKEN']
    os.environ['OPENAI_API_KEY'] = os.environ['INPUT_OPENAI_API_KEY']
    base_branch = os.environ['INPUT_BASE_BRANCH']
    issue_number = int(os.environ['INPUT_ISSUE_NUMBER'])
    issue_title = os.environ['INPUT_ISSUE_TITLE']
    issue_body = os.environ['INPUT_ISSUE_BODY']

    from autopr.main import main
    main(
        github_token=github_token,
        repo_path=repo_path,
        base_branch_name=base_branch,
        issue_number=issue_number,
        issue_title=issue_title,
        issue_body=issue_body,
    )
