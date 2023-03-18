from typing import Callable

import openai
from git import Tree

import guardrails as gd

from pr_drafter.models import PullRequest, Commit


class GenerationService:
    def generate_pr(self, repo_tree: Tree, issue_title: str, issue_body: str, issue_number: int) -> PullRequest:
        raise NotImplementedError

    @staticmethod
    def repo_to_codebase(tree: Tree, filepath_list: list[str] = None):
        # Concatenate all the files in the repo,

        codebase = ""
        for blob in tree.traverse():
            # Only include files in filepath_list
            if filepath_list is not None and blob.path not in filepath_list:
                continue

            # Skip directories
            if blob.type == 'tree':
                continue

            # Skip lock file
            if any(
                blob.path.endswith(ending)
                for ending in ['.lock']
            ):
                continue

            # Separate files with a newline
            if codebase:
                codebase += "\n"

            # Add path
            codebase += f"Path: {blob.path}\n"

            # Add file contents, with line numbers
            blob_text = blob.data_stream.read().decode()
            for i, line in enumerate(blob_text.split('\n')):
                codebase += f"{i+1} {line}\n"

        return codebase


class RailsGenerationService(GenerationService):
    rail_spec = f"""
<rail version="0.1">
<output>
{PullRequest.rail_spec}
</output>
<prompt>
Oh skilled senior software developer, with all your programming might and wisdom, please write a pull request for me.
This is the codebase subset we decided to look at:
```{{{{codebase}}}}```

Please address the following issue:
```{{{{issue}}}}```

@xml_prefix_prompt

{{output_schema}}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
    """
    file_select_spec = f"""
<rail version="0.1">
<output>
    <list name="filepaths">
        <string
            description="The path to the file in the repo."
            format="filepath"
            on-fail="reask"
        />
    </list>
</output>
<prompt>
Oh skilled senior software developer, with all your programming might and wisdom, let's write a pull request.

This is the list of files in the repo:
```{{{{files}}}}```

This is the issue that was opened:
```{{{{issue}}}}```

Which files should we take a look at?

@xml_prefix_prompt

{{output_schema}}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""
    pr_verification_spec = f"""
<rail version="0.1">
<output>
{PullRequest.rail_spec}
</output>
<prompt>
Oh skilled senior software developer, with all your programming might and wisdom, please make sure that this pull request addresses the issue, and is accurately described.

This is the codebase subset we decided to look at:
```{{{{codebase}}}}```

This is the issue that was opened:
```{{{{issue}}}}```

This is the pull request that was generated:
```{{{{pull_request}}}}```

@xml_prefix_prompt

{{output_schema}}

@json_suffix_prompt_v2_wo_none
</prompt>
</rail>
"""

    def __init__(
        self,
        max_tokens: int = 1000,
        completion_func: Callable = openai.ChatCompletion.create,
        completion_model: str = 'gpt-4',
        num_reasks: int = 3,
    ):
        self.max_tokens = max_tokens
        self.completion_func = completion_func
        self.completion_model = completion_model
        self.num_reasks = num_reasks

    def get_filepath_list(self, repo_tree: Tree, issue_text: str) -> list[str]:
        pr_guard = gd.Guard.from_rail_string(
            self.file_select_spec,  # make sure to import custom validators before this
            num_reasks=self.num_reasks,
        )
        list_of_files = "\n".join(
            blob.path
            for blob in repo_tree.traverse()
            if blob.type != 'tree'
        )
        print('Getting filepaths to look at...')
        raw_o, dict_o = pr_guard(
            self.completion_func,
            model=self.completion_model,
            max_tokens=self.max_tokens,
            prompt_params={
                'files': list_of_files,
                'issue': issue_text,
            },
        )
        if dict_o is None:
            raise RuntimeError("No valid list of files generated", raw_o)
        print(f'Got filepaths:')
        for filepath in dict_o['filepaths']:
            print(f' -  {filepath}')
        return dict_o['filepaths']

    def generate_pr(self, repo_tree: Tree, issue_title: str, issue_body: str, issue_number: int) -> PullRequest:
        issue_text = f"Issue #{str(issue_number)}\nTitle: {issue_title}\n\n{issue_body}"

        # Get the list of files to look at
        pr_guard = gd.Guard.from_rail_string(
            self.rail_spec,  # make sure to import custom validators before this
            num_reasks=self.num_reasks,
        )
        filepath_list = self.get_filepath_list(repo_tree, issue_text)
        codebase = self.repo_to_codebase(repo_tree, filepath_list)

        # Generate the PR
        raw_o, dict_o = pr_guard(
            self.completion_func,
            model=self.completion_model,
            max_tokens=self.max_tokens,
            prompt_params={
                'codebase': codebase,
                'issue': issue_text
            },
        )
        if dict_o is None:
            raise RuntimeError("No valid PR generated", raw_o)
        pr_model = PullRequest.parse_obj(dict_o['pull_request'])

        # Print the PR
        print('Generated preliminary PR:')
        print(f"Title: {pr_model.title}")
        print(f"Body: {pr_model.initial_message}")
        for commit in pr_model.commits:
            print(f"Commit message: {commit.message}")
            print(f"Commit diff: {commit.diff}")

        # Verify if the PR is valid
        pr_guard = gd.Guard.from_rail_string(
            self.pr_verification_spec,  # make sure to import custom validators before this
            num_reasks=self.num_reasks,
        )
        raw_o, dict_o = pr_guard(
            self.completion_func,
            model=self.completion_model,
            max_tokens=self.max_tokens,
            prompt_params={
                'codebase': codebase,
                'issue': issue_text,
                'pull_request': pr_model.json(),
            },
        )
        if dict_o is None:
            raise RuntimeError("PR verification failed", raw_o)
        pr_model = PullRequest.parse_obj(dict_o['pull_request'])

        # Print the PR
        print('Verified the PR:')
        print(f"Title:\n{pr_model.title}\n")
        print(f"Body:\n{pr_model.initial_message}\n")
        for commit in pr_model.commits:
            print(f"Commit message:\n{commit.message}\n")
            print(f"Commit diff:\n{commit.diff}")


# from langchain import LLMChain
# from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
# from langchain.chat_models import ChatOpenAI
#
# class SingleLangchainGenerationService(GenerationService):
#     system_message_template = SystemMessagePromptTemplate.from_template(
#         "You are a helpful contributor to the project, tasked with preparing pull requests for issues."
#     )
#     human_template = HumanMessagePromptTemplate.from_template("""
# Given the following codebase:
# {codebase}
#
# And the following issue:
# Title: {issue_title}
# Body: {issue_body}
#
# ONLY return a valid git patch (no other text is necessary). Omit the `index 0000000..0000000` line.
#     """)
#
#     def generate_patch(self, repo_tree: Tree, issue_title: str, issue_body: str) -> str:
#         codebase = self.repo_to_codebase(repo_tree)
#         chat = ChatOpenAI(temperature=0)
#         chat_prompt = ChatPromptTemplate.from_messages([
#             self.system_message_template,
#             self.human_template,
#         ])
#
#         chain = LLMChain(llm=chat, prompt=chat_prompt, verbose=True)
#         return chain.run(
#             codebase=codebase,
#             issue_title=issue_title,
#             issue_body=issue_body,
#         )
#
#     def generate_pr(self, repo_tree: Tree, issue_title: str, issue_body: str) -> PullRequest:
#         patch = self.generate_patch(repo_tree, issue_title, issue_body)
#         # TODO describe the patch in the PR body
#         return PullRequest(
#             title=f"Fix {issue_title}",
#             body="",
#             commits=[
#                 Commit(
#                     message=f"Fix {issue_title}",
#                     diff=patch,
#                 )
#             ],
#         )
