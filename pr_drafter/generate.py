import openai
from git import Repo, Tree

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


def repo_to_codebase(tree: Tree):
    # Concatenate all the files in the repo,

    codebase = ""
    for blob in tree.traverse():
        # If the blob is not a code file, skip it
        if not any(
            blob.path.endswith(ending)
            for ending in ['.py', '.md']
        ):
            continue
        codebase += f"Path: {blob.path}\n```{blob.data_stream.read().decode()}\n```\n"
    return codebase


def generate_pr(repo_tree: Tree, issue_title: str, issue_body: str) -> PullRequest:
    codebase = repo_to_codebase(repo_tree)
    smth = pr_guard(
        openai.Completion.create,
        model='text-davinci-003',
        prompt_params={
            'codebase': codebase,
            'issue': f"Title: {issue_title}\nBody: {issue_body}",
        },
    )
    return PullRequest.parse_obj(smth[1])
