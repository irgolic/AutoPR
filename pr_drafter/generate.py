import openai
from git import Repo

import guardrails as gd
from pr_drafter.models import PullRequest


rail_spec = f"""
<rail version="0.1">
<output>
{PullRequest.rail_spec}
</output>
<prompt>
Given the following codebase:

{{{{codebase}}}}

And the following issue:

{{{{issue}}}}

Generate a pull request that addresses the issue.

@xml_prefix_prompt

{{output_schema}}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""
pr_guard = gd.Guard.from_rail_string(rail_spec)


def repo_to_codebase(repo: Repo):
    # Concatenate all the files in the repo,
    # Describing them by prepending `Path: <path>`
    # and appending `@end_of_file`
    #
    # Example:
    # Path: pr_drafter/generate.py
    # ...
    # @end_of_file
    # Path: pr_drafter/models.py
    # ...
    # @end_of_file

    tree = repo.tree()
    codebase = ""
    for blob in tree.traverse():
        # If the blob is not a code file, skip it
        if not blob.path.endswith(".py"):
            continue
        codebase += f"Path: {blob.path}\n{blob.data_stream.read().decode()}\n@end_of_file\n"
    return codebase


def generate_pr(repo: Repo, issue_title: str, issue_body: str) -> PullRequest:
    codebase = repo_to_codebase(repo)
    smth = pr_guard(
        openai.Completion.create,
        codebase=codebase,
        issue=f"Title: {issue_title}\nBody: {issue_body}",
    )
    return PullRequest.parse_obj(smth[1])
