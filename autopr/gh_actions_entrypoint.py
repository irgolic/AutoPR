import json
import os

from autopr.log_config import configure_logging
configure_logging()

import structlog
log = structlog.get_logger()


if __name__ == '__main__':
    log.info("Starting gh_actions_entrypoint.py")

    repo_path = os.environ['GITHUB_WORKSPACE']

    os.environ['OPENAI_API_KEY'] = os.environ['INPUT_OPENAI_API_KEY']

    event_json = os.environ['INPUT_EVENT']
    event = json.loads(event_json)
    log.info("Github event", gh_event=event)

    inputs = {
        'github_token': os.environ['INPUT_GITHUB_TOKEN'],
        'base_branch': os.environ['INPUT_BASE_BRANCH'],
        'issue_number': int(event['issue']['number'])
        'issue_title': event['issue']['title'],
        'issue_body': event['issue']['body'],
        'model': os.environ['INPUT_MODEL'],
        'context_limit': int(os.environ['INPUT_CONTEXT_LIMIT']),
        'min_tokens': int(os.environ['INPUT_MIN_TOKENS']),
        'max_tokens': int(os.environ['INPUT_MAX_TOKENS']),
        'num_reasks': int(os.environ['INPUT_NUM_REASKS']),
        'pull_request_agent_id': os.environ['INPUT_PULL_REQUEST_AGENT_ID'],
        'codegen_agent_id': os.environ['INPUT_CODEGEN_AGENT_ID'],
    }
    inputs.update({
        k: v
        for k, v in os.environ.items()
        if k.startswith('INPUT_') and k[6:].lower() not in inputs and 'API_KEY' not in k
    })

    from autopr.main import main
    main(
        repo_path=repo_path,
        **inputs
    )
