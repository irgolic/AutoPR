import asyncio
import fnmatch
import os
import re
from collections import defaultdict
from typing import Literal, Optional
from unittest.mock import patch
import pydantic
import yaml

from autopr.actions.base import Action
from autopr.models.artifacts import Issue

from autopr.services.platform_service import PlatformService
from tree_sitter_languages import get_parser
from tree_sitter import Parser


comment_treesitter_language_mapping = {
    "python": ["#"],
    "javascript": ["//", "/*"],
}


class TodoLocation(pydantic.BaseModel):
    filepath: str
    start_line: int
    end_line: int
    url: str


class Todo(pydantic.BaseModel):
    task: str
    locations: list[TodoLocation]
    fingerprint: str
    issue: Optional[Issue] = None


class Inputs(pydantic.BaseModel):
    language: Literal[tuple(comment_treesitter_language_mapping.keys())] = "python"  # type: ignore
    todo_keywords: list[str] = ["TODO", "FIXME"]
    ignored_paths: list[str] = pydantic.Field(default_factory=list)


class Outputs(pydantic.BaseModel):
    todos: list[Todo]


class FindTodos(Action[Inputs, Outputs]):
    """
    Scan through all files in a directory and its subdirectories
    and returns a list of all comments with "#TODO" or "#FIXME" in
    them and prints them out in a list with the task, filepath and line as defined in Outputs.
    """

    id = "find_todos"

    @staticmethod
    def is_binary(path: str):
        return b"\x00" in open(path, "rb").read(1024)

    async def process_file(
        self, file: str, todo_keywords: list[str], comment_keywords: list[str], parser: Parser
    ) -> dict[str, list[TodoLocation]]:
        if self.is_binary(file):
            return {}

        task_to_locations = defaultdict(list)

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            file_content = f.read()

        # Parse the file with Tree-sitter
        tree = parser.parse(bytes(file_content, "utf8"))
        root_node = tree.root_node

        async def process_comment(node):
            comment_text = file_content[node.start_byte : node.end_byte].strip()
            combined_todo_keywords = "|".join(todo_keywords)

            for comment in comment_keywords:
                pattern = re.compile(rf"^{re.escape(comment)}\s*({combined_todo_keywords})")

                if not pattern.search(comment_text):
                    continue

                # Check if this comment continues in the next line
                task = re.sub(rf"^{re.escape(comment)}\s*", "", comment_text)
                start_line = node.start_point[0] + 1
                end_line = node.end_point[0] + 1
                next_node = node.next_named_sibling
                if next_node:
                    comment_text_next = file_content[
                        next_node.start_byte : next_node.end_byte
                    ].strip()
                    comment_pattern_next = re.compile(rf"^{re.escape(comment)}\s{{2,}}(.+)$")
                    while (
                        next_node
                        and next_node.type == "comment"
                        and node.start_point[0] + 1 == next_node.start_point[0]
                        and comment_pattern_next.search(comment_text_next)
                    ):
                        task += " " + re.sub(rf"^{re.escape(comment)}\s*", "", comment_text_next)
                        end_line = next_node.end_point[0] + 1
                        next_node = next_node.next_named_sibling

                location = await self.get_todo_location(file, start_line, end_line)
                task_to_locations[task].append(location)

        async def traverse(node):
            """A simple recursive function to traverse all nodes and find comments"""
            if node.type == "comment":
                await process_comment(node)

            # Recursively traverse children
            for child in node.children:
                await traverse(child)

        await traverse(root_node)
        return task_to_locations

    async def get_todo_location(self, file, start_line, end_line) -> TodoLocation:
        branch_name = self.publish_service.base_branch
        url = await self.platform_service.get_file_url(
            file, branch_name, start_line=start_line, end_line=end_line, margin=5
        )
        location = TodoLocation(filepath=file, start_line=start_line, end_line=end_line, url=url)
        return location

    async def filter_closed_issues(self, todos: list[Todo], issues: list[Issue]) -> list[Todo]:
        closed_issues_list = await self.platform_service.get_issues(state="closed")
        closed_issue_bodies = [closed_issue.messages[0].body for closed_issue in closed_issues_list]
        filtered_todos = [
            todo
            for todo in todos
            if not any(todo.task in closed_issue_body for closed_issue_body in closed_issue_bodies)
        ]
        return filtered_todos

    def parse_todo_issues(self, issues: list[Issue]) -> dict[str, Issue]:
        todo_issues = {}
        for issue in issues:
            if not issue.messages:
                continue
            body = issue.messages[0].body
            if not body.startswith("<!--") or "-->" not in body:
                continue
            # load yaml between <!-- and -->
            yaml_str = body.split("-->")[0].split("<!--")[1]
            try:
                yaml_dict = yaml.safe_load(yaml_str)
            except yaml.YAMLError:
                continue
            if not yaml_dict or yaml_dict.get("issue_type") != "TODO" or "task" not in yaml_dict:
                continue
            task = yaml_dict["task"]

            self.log.info(f"Found TODO issue {issue.number} for task {task}")

            if task in todo_issues and todo_issues[task].open:
                if issue.open:
                    self.log.error(f"Duplicate open TODO issue for task {task}")
                self.log.debug(f"Skipping TODO issue {issue.number}")
                continue
            todo_issues[task] = issue
        return todo_issues

    @staticmethod
    def get_todo_fingerprint(task: str) -> str:
        fingerprint_dict = {
            "info": "AutoPR fingerprint",
            "issue_type": "TODO",
            "task": task,
        }
        return yaml.dump(fingerprint_dict, sort_keys=False)

    async def close_not_used_issues(self, issues: list[Issue], todos: list[Todo]) -> None:
        todo_issues = [todo.issue for todo in todos if todo.issue]
        for issue in issues:
            if issue.open and issue not in todo_issues:
                self.log.debug(f"Closing issue {issue.number} because it is not referenced anymore")
                await self.platform_service.close_issue(issue.number)

    async def run(self, inputs: Inputs) -> Outputs:
        # Set the parsing language
        if inputs.language not in comment_treesitter_language_mapping:
            raise ValueError(f"Language {inputs.language} not supported")

        comment_keywords = comment_treesitter_language_mapping[inputs.language]
        parser = get_parser(inputs.language)
        current_dir = os.getcwd()
        task_to_locations = {}

        for root, dirs, files in os.walk(current_dir):
            if ".git" in dirs:
                dirs.remove(".git")
            if ".git" in files:
                files.remove(".git")

            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), current_dir)

                if any(fnmatch.fnmatch(relative_path, pattern) for pattern in inputs.ignored_paths):
                    continue

                file_task_to_locations = await self.process_file(
                    relative_path, inputs.todo_keywords, comment_keywords, parser
                )

                for task, locations in file_task_to_locations.items():
                    task_to_locations.setdefault(task, []).extend(locations)

        issues = await self.platform_service.get_issues()
        issue_for_task = self.parse_todo_issues(issues)

        todos = [
            Todo(
                task=task,
                locations=locations,
                issue=issue_for_task.get(task),
                fingerprint=self.get_todo_fingerprint(task),
            )
            for task, locations in task_to_locations.items()
        ]
        await self.close_not_used_issues(issues, todos)

        sorted_todos = sorted(todos, key=lambda todo: todo.task)  # This simplifies testing

        filtered_todos = [todo for todo in sorted_todos if todo.issue is None or todo.issue.open]

        return Outputs(todos=filtered_todos)


# When you run this file
if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    with patch.object(PlatformService, "get_file_url", return_value="https://github.com/") as mock:
        asyncio.run(
            # Run the action manually
            run_action_manually(action=FindTodos, inputs=Inputs(), repo_resource="repo_with_todos")
        )
