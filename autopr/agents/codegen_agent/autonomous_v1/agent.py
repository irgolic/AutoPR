import os
import tempfile
from collections import defaultdict
from typing import Optional
from git.repo import Repo

from autopr.agents.codegen_agent import CodegenAgentBase
from autopr.agents.codegen_agent.autonomous_v1.action_utils.context import ContextFile, ContextCodeHunk
from autopr.agents.codegen_agent.autonomous_v1.action_utils.file_changes import GeneratedFileHunk, NewFileChain, RewriteCodeHunkChain
from autopr.agents.codegen_agent.autonomous_v1.actions import Action, MakeDecision, NewFileAction, ActionUnion, \
    EditFileAction
from autopr.models.artifacts import DiffStr, Issue, Message
from autopr.models.rail_objects import CommitPlan, PullRequestDescription, FileHunk
from autopr.repos.completions_repo import OpenAIChatCompletionsRepo
from autopr.services.chain_service import ChainService
from autopr.services.commit_service import CommitService
from autopr.services.diff_service import DiffService, PatchService, GitApplyService
from autopr.services.publish_service import PublishService
from autopr.services.rail_service import RailService


class AutonomousCodegenAgent(CodegenAgentBase):
    id = "auto-v1"

    def __init__(
        self,
        *args,
        context_size: int = 3,
        iterations_per_commit: int = 5,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.context_size = context_size
        self.iterations_per_commit = iterations_per_commit

    @staticmethod
    def _split_into_lines(text: str) -> list[str]:
        lines = text.splitlines()
        # If text ends with a newline, we want to keep that as a line
        if text.rstrip() != text:
            lines.append("")
        return lines

    def _get_lines(
        self,
        repo: Repo,
        filepath: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> Optional[list[tuple[int, str]]]:
        working_dir = repo.working_tree_dir
        assert working_dir is not None
        path = os.path.join(working_dir, filepath)
        if not os.path.exists(path):
            self.log.error(f"File {filepath} not in repo")
            return None

        with open(path, 'r') as f:
            lines = self._split_into_lines(f.read())
        code_hunk: list[tuple[int, str]] = []

        # Get and limit line numbers
        start_line = start_line or 1
        start_line = min(max(start_line, 1), len(lines))
        end_line = end_line or len(lines)
        end_line = min(max(end_line, 1), len(lines))
        end_line = max(start_line, end_line)

        for line_num in range(start_line, end_line + 1):
            code_hunk.append((line_num, lines[line_num - 1]))
        return code_hunk

    def _make_context(
        self,
        repo: Repo,
        commit: CommitPlan,
    ) -> list[ContextFile]:
        hunks_by_filepath = defaultdict(list)
        for hunk in commit.relevant_file_hunks:
            fp = hunk.filepath
            hunks_by_filepath[fp].append(hunk)

        context = []
        for fp, hunks in hunks_by_filepath.items():
            code_hunks = []
            for hunk in hunks:
                lines = self._get_lines(
                    repo=repo,
                    filepath=fp,
                    start_line=hunk.start_line,
                    end_line=hunk.end_line,
                )
                if lines is None:
                    continue
                code_hunks.append(
                    ContextCodeHunk(
                        code_hunk=lines,
                    )
                )

            if code_hunks:
                context.append(
                    ContextFile(
                        filepath=fp,
                        code_hunks=code_hunks,
                    )
                )

        return context

    def _create_new_file(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
        context: list[ContextFile],
        new_file_action: NewFileAction,
    ) -> str:
        self.publish_service.update_section(title=f"Creating new file: {new_file_action.filepath}")
        # Check if file exists
        repo_path = repo.working_tree_dir
        assert repo_path is not None
        filepath = os.path.join(repo_path, new_file_action.filepath)
        if os.path.exists(filepath):
            self.log.warning("File already exists, skipping", filepath=filepath)
            return "File already exists, skipping"
        # Check if filename is a directory (doesnt exist yet)
        if os.path.basename(filepath) == "":
            self.log.warning("File is a directory, skipping", filepath=filepath)
            return "Filepath is a directory, skipping. Directories will be created automatically."

        # Run new file langchain
        new_file_chain = NewFileChain(
            issue=issue,
            pull_request_description=pr_desc,
            commit=current_commit,
            context_hunks=context,
            plan=new_file_action.description,
        )
        new_file_hunk: Optional[GeneratedFileHunk] = self.chain_service.run_chain(new_file_chain)
        if new_file_hunk is None:
            self.log.error("Failed to generate new file")
            return "Failed to generate new file"

        # Create dirs
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath, exist_ok=True)
        # Write file
        path = os.path.join(repo_path, filepath)
        with open(path, "w") as f:
            f.write(new_file_hunk.contents)
        self.publish_service.update_section(title=f"Created new file: {new_file_action.filepath}")
        return new_file_hunk.outcome

    def _edit_existing_file(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
        context: list[ContextFile],
        edit_file_action: EditFileAction,
    ) -> str:
        # Check if file exists
        repo_path = repo.working_tree_dir
        assert repo_path
        filepath = os.path.join(repo_path, edit_file_action.filepath)
        if not os.path.exists(filepath):
            self.log.warning("File does not exist, creating file instead", filepath=filepath)
            create_file_action = NewFileAction(
                filepath=edit_file_action.filepath,
                description=edit_file_action.description,
            )
            effect = self._create_new_file(repo, issue, pr_desc, current_commit, context, create_file_action)
            return "File does not exist, creating instead: " + effect
        self.publish_service.update_section(title=f"Editing existing file: {edit_file_action.filepath}")

        # Grab file contents
        with open(filepath, "r") as f:
            lines = self._split_into_lines(f.read())

        # Get relevant hunk
        start_line, end_line = edit_file_action.start_line, edit_file_action.end_line
        if not lines:
            code_hunk = ContextCodeHunk(
                code_hunk=[],
            )
            indent = 0
        elif start_line is None or end_line is None:
            line_nums = list(range(1, len(lines) + 1))
            code_hunk = ContextCodeHunk(
                code_hunk=list(zip(line_nums, lines)),
                highlight_line_numbers=line_nums,
            )
            indent = 0
        else:
            # Limit line numbers
            start_line, end_line = min(max(start_line, 1), len(lines)), min(max(end_line, 1), len(lines))
            end_line = max(start_line, end_line)

            code_hunk_lines: list[tuple[int, str]] = []
            context_start_line = max(1, start_line - self.context_size)
            context_end_line = min(len(lines), end_line + self.context_size)
            for line_num in range(context_start_line, context_end_line + 1):
                code_hunk_lines.append((line_num, lines[line_num - 1]))
            highlight_line_nums = list(range(start_line, end_line + 1))
            code_hunk = ContextCodeHunk(
                code_hunk=code_hunk_lines,
                highlight_line_numbers=highlight_line_nums,
            )

            # Find the indentation common to all highlighted lines in the hunk
            highlighted_lines = [
                lines[line_num - 1]
                for line_num in highlight_line_nums
            ]
            lines_for_indent = [
                len(line) - len(line.lstrip())
                for line in highlighted_lines
                if line.strip()
            ]
            if not lines_for_indent:
                indent = 0
            else:
                indent = min(lines_for_indent)

        # Run edit file langchain
        edit_file_chain = RewriteCodeHunkChain(
            issue=issue,
            pull_request_description=pr_desc,
            commit=current_commit,
            context_hunks=context,
            hunk_contents=code_hunk,
            plan=edit_file_action.description,
        )
        edit_file_hunk: Optional[GeneratedFileHunk] = self.chain_service.run_chain(edit_file_chain)
        if edit_file_hunk is None:
            self.log.error("Failed to edit file")
            self.publish_service.update_section(title=f"Failed to edit file: {edit_file_action.filepath}")
            return "Failed to edit file"

        # Add indentation to new lines
        new_lines = []
        for line in self._split_into_lines(edit_file_hunk.contents):
            if not line.strip():
                new_lines.append("")
                continue
            new_lines.append(" " * indent + line)

        # Replace lines in file
        if start_line is not None and end_line is not None:
            lines = lines[:start_line - 1] + new_lines + lines[end_line:]
        else:
            lines = new_lines

        # Write file
        path = os.path.join(repo_path, filepath)
        with open(path, "w") as f:
            f.write("\n".join(lines))

        self.publish_service.update_section(title=f"Edited existing file: {edit_file_action.filepath}")
        return edit_file_hunk.outcome

    def _generate_changes(
        self,
        repo: Repo,
        issue: Issue,
        pr_desc: PullRequestDescription,
        current_commit: CommitPlan,
    ) -> None:
        actions_history: list[tuple[ActionUnion, str]] = []
        for _ in range(self.iterations_per_commit):
            # Show relevant code, determine what hunks to change
            context = self._make_context(repo, current_commit)

            # Declare decision making
            self.publish_service.start_section("Deciding what action to take")

            # Choose action
            action_rail = MakeDecision(
                issue=issue,
                pull_request_description=pr_desc,
                commit=current_commit,
                context_hunks=context,
                past_actions=actions_history,
            )
            action = self.rail_service.run_prompt_rail(action_rail)
            if action is None or not isinstance(action, Action):
                self.log.error("Action choice failed")
                self.publish_service.end_section("Error (invalid action choice)")
                break

            # Run action
            if action.action == "new_file":
                if action.new_file is None:
                    self.log.error("No new file action")
                    self.publish_service.end_section("Error (invalid new file action)")
                    break
                action_obj = action.new_file
                effect = self._create_new_file(repo, issue, pr_desc, current_commit, context, action_obj)
            elif action.action == "edit_file":
                if action.edit_file is None:
                    self.log.error("No edit file action")
                    self.publish_service.end_section("Error (invalid edit file action)")
                    break
                action_obj = action.edit_file
                effect = self._edit_existing_file(repo, issue, pr_desc, current_commit, context, action_obj)
            elif action.action == "finished":
                self.log.info("Finished writing commit")
                msg = action.commit_message
                if msg is not None:
                    current_commit.commit_message = msg
                    self.publish_service.end_section(f"Finished writing commit: {msg}")
                    self.publish_service.update_section(title=msg)
                else:
                    self.publish_service.end_section("Finished writing commit")
                break
            else:
                self.log.error(f"Unknown action {action.action}")
                self.publish_service.end_section(f"Error (unknown action {action.action})")
                break

            # Add the file into the context of the rest of the commits, if it's not yet there
            if not any(action_obj.filepath == fh.filepath for fh in current_commit.relevant_file_hunks):
                current_commit.relevant_file_hunks.append(
                    FileHunk(
                        filepath=action_obj.filepath,
                    )
                )

            # TODO add diff to result
            self.publish_service.end_section()

            actions_history.append((action_obj, effect))


if __name__ == '__main__':
    import json
    pull_request_json = """{
    "title": "Implementing Doom game in Python",
    "body": "Hi there! I've addressed the issue of creating a Doom game in Python. I have created a new file called doom.py which contains the implementation of the game. This game is really cool and will provide a great experience to the player. I hope you will like it. Please review my code and let me know if there are any changes that need to be made. Thanks.",
    "commits": [
        {
            "commit_message": "Initial commit - Added template for doom game - doom.py",
            "relevant_file_hunks": [
                {
                    "filepath": "doom.py"
                }
            ],
            "commit_changes_description": ""
        },
        {
            "commit_message": "Implemented player controls - doom.py",
            "relevant_file_hunks": [
                {
                    "filepath": "doom.py"
                }
            ],
            "commit_changes_description": ""
        },
        {
            "commit_message": "Added game mechanics - doom.py",
            "relevant_file_hunks": [
                {
                    "filepath": "doom.py"
                }
            ],
            "commit_changes_description": ""
        },
        {
            "commit_message": "Implemented scoring system - doom.py",
            "relevant_file_hunks": [
                {
                    "filepath": "doom.py"
                }
            ],
            "commit_changes_description": ""
        },
        {
            "commit_message": "Added sound effects - doom.py",
            "relevant_file_hunks": [
                {
                    "filepath": "doom.py"
                }
            ],
            "commit_changes_description": ""
        }
    ]
}"""
    pull_request = json.loads(pull_request_json)
    pr_desc = PullRequestDescription(**pull_request)
    issue = Issue(
        number=1,
        title="Add Doom game in Python",
        author="jameslamb",
        messages=[
            Message(
                author="jameslamb",
                body="Make a cool doom game",
            ),
        ],
    )
    # make tmpdir
    with tempfile.TemporaryDirectory() as tmpdir:
        # init repo
        repo = Repo.init(tmpdir)
        # create branch
        repo.git.checkout("-b", "main")
        # create commit
        repo.git.commit("--allow-empty", "-m", "Initial commit")

        completions_repo = OpenAIChatCompletionsRepo(
            model="gpt-4",
        )
        commit_service = CommitService(
            repo,
            repo_path=tmpdir,
            branch_name="hah",
            base_branch_name="main",
        )
        publish_service = PublishService(
            issue=issue,
        )
        rail_service = RailService(
            publish_service=publish_service,
            completions_repo=completions_repo,
        )
        diff_service = GitApplyService(repo)

        chain_service = ChainService(
            publish_service=publish_service,
            completions_repo=completions_repo,
        )
        codegen_agent = AutonomousCodegenAgent(
            publish_service=publish_service,
            rail_service=rail_service,
            chain_service=chain_service,
            diff_service=diff_service,
            repo=repo,
        )
        for c in pr_desc.commits:
            # codegen_agent.generate_changes(repo, issue, pr_desc, c)
            commit_service.commit(c, push=False)
