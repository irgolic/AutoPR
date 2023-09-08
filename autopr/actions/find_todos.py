import asyncio
import os
import re
from unittest.mock import patch
import pydantic
from autopr.actions.base import Action

from typing import List

from autopr.services.platform_service import PlatformService


class TodoLocation(pydantic.BaseModel):
    filepath: str
    start_line: int
    end_line: int
    url: str


class Todo(pydantic.BaseModel):
    task: str
    locations: List[TodoLocation]


class Inputs(pydantic.BaseModel):
    comment: str = "#"
    todo_keywords: list[str] = ["TODO", "FIXME"]


class Outputs(pydantic.BaseModel):
    todos: List[Todo]


class FindTodos(Action[Inputs, Outputs]):
    """
    Scan through all files in a directory and its subdirectories 
    and returns a list of all comments with "#TODO" or "#FIXME" in 
    them and prints them out in a list with the task, filepath and line as defined in Outputs.
    """
    id = "find_todos"

    @staticmethod
    def is_binary(path):
        return b"\x00" in open(path, "rb").read(1024)

    async def process_file(self, file, inputs) -> dict[str, List[TodoLocation]]:
        if self.is_binary(file):
            return {}
        
        task_to_locations = {}
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            contents = f.readlines()

            in_multiline_comment = False
            task = ""
            multiline_start_line = 0

            line_number = 0
            for line_number, line in enumerate(contents):
                stripped_line = line.strip()

                combined_todo_keywords = "|".join(inputs.todo_keywords)
                comment_type = inputs.comment

                pattern = re.compile(rf'{comment_type}\s*({combined_todo_keywords})')

                if pattern.search(stripped_line) and not in_multiline_comment:
                    in_multiline_comment = True
                    task = stripped_line.lstrip(comment_type).lstrip()
                    multiline_start_line = line_number + 1

                elif in_multiline_comment and stripped_line.startswith(comment_type + "  "):
                    task += " " + stripped_line[len(comment_type) + 2:].lstrip()

                elif in_multiline_comment:
                    location = await self.get_todo_location(file, multiline_start_line, line_number)
                    task_to_locations.setdefault(task, []).append(location)
                    in_multiline_comment = False
                    task = ""

            if in_multiline_comment:
                location = await self.get_todo_location(file, multiline_start_line, line_number + 1)
                task_to_locations.setdefault(task, []).append(location)

        return task_to_locations


    async def get_todo_location(self, file, start_line, end_line) -> TodoLocation:
        branch_name = self.publish_service.base_branch
        url = await self.platform_service.get_file_url(file, branch_name, start_line=start_line, end_line=end_line, margin=5)
        location = TodoLocation(filepath=file, start_line=start_line, end_line=end_line, url=url)
        return location

    async def run(self, inputs: Inputs) -> Outputs:
        current_dir = os.getcwd()
        all_task_to_locations = {}

        for root, dirs, files in os.walk(current_dir):
            if ".git" in dirs:
                dirs.remove(".git")
            if ".git" in files:
                files.remove(".git")

            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), current_dir)
                file_task_to_locations = await self.process_file(relative_path, inputs)

                for task, locations in file_task_to_locations.items():
                    all_task_to_locations.setdefault(task, []).extend(locations)

        todos = [Todo(task=task, locations=locations) for task, locations in all_task_to_locations.items()]
        return Outputs(todos=todos)


# When you run this file
if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    with patch.object(PlatformService, "get_file_url", return_value="https://github.com/") as mock:
        asyncio.run(
            # Run the action manually
            run_action_manually(
                action=FindTodos,
                inputs=Inputs(),
                repo_resource="repo_with_todos"
            )
        )
