import asyncio
import os
import re
from unittest.mock import patch
import pydantic
from autopr.actions.base import Action

from autopr.services.platform_service import PlatformService
from tree_sitter import Language, Parser


# Initialize the tree-sitter language parser
Language.build_library(
    'build/my-languages.so',
    [
        'tree-sitter-languages/tree-sitter-python',
        'tree-sitter-languages/tree-sitter-javascript'
    ]
)

comment_treesitter_language_mapping = {
    "#": "python",
    "//": "javascript",
    "/*": "javascript",
}

parser = Parser()
# The language gets set in the method run


class TodoLocation(pydantic.BaseModel):
    filepath: str
    start_line: int
    end_line: int
    url: str


class Todo(pydantic.BaseModel):
    task: str
    locations: list[TodoLocation]


class Inputs(pydantic.BaseModel):
    comment: str = "#"
    todo_keywords: list[str] = ["TODO", "FIXME"]


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
    def is_binary(path):
        return b"\x00" in open(path, "rb").read(1024)

    async def process_file(self, file, inputs) -> dict[str, list[TodoLocation]]:
        if self.is_binary(file):
            return {}

        task_to_locations = {}

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            file_content = f.read()

        # Parse the file with Tree-sitter
        tree = parser.parse(bytes(file_content, "utf8"))
        root_node = tree.root_node

        # A simple recursive function to traverse all nodes and find comments
        async def traverse(node):
            nonlocal file_content
            if node.type == "comment":
                comment_text = file_content[node.start_byte:node.end_byte].strip()
                combined_todo_keywords = "|".join(inputs.todo_keywords)
                pattern = re.compile(rf'^{re.escape(inputs.comment)}\s*({combined_todo_keywords})')

                if pattern.search(comment_text):
                    # Check if this comment continues in the next line
                    task = re.sub(rf'^{re.escape(inputs.comment)}\s*', '', comment_text)
                    start_line = node.start_point[0] + 1
                    end_line = node.end_point[0] + 1
                    next_node = node.next_named_sibling
                    if next_node:
                        comment_text_next = file_content[next_node.start_byte:next_node.end_byte].strip()
                        comment_pattern_next = re.compile(rf'^{re.escape(inputs.comment)}\s{{2,}}(.+)$')
                        while next_node and next_node.type == "comment" and node.start_point[0] + 1 == next_node.start_point[0] and comment_pattern_next.search(comment_text_next):
                            task += " " + re.sub(rf'^{re.escape(inputs.comment)}\s*', '', comment_text_next)
                            end_line = next_node.end_point[0] + 1
                            next_node = next_node.next_named_sibling

                    location = await self.get_todo_location(file, start_line, end_line)
                    task_to_locations.setdefault(task, []).append(location)

            # Recursively traverse children
            for child in node.children:
                await traverse(child)

        await traverse(root_node)
        return task_to_locations


    async def get_todo_location(self, file, start_line, end_line) -> TodoLocation:
        branch_name = self.publish_service.base_branch
        url = await self.platform_service.get_file_url(file, branch_name, start_line=start_line, end_line=end_line, margin=5)
        location = TodoLocation(filepath=file, start_line=start_line, end_line=end_line, url=url)
        return location

    async def run(self, inputs: Inputs) -> Outputs:
        # Set the parsing language
        if not comment_treesitter_language_mapping.get(inputs.comment):
            raise ValueError(f"Comment {inputs.comment} not supported. Current supported comments are: {', '.join(list(comment_treesitter_language_mapping.keys()))}")
        PARSER_LANGUAGE = Language('build/my-languages.so', comment_treesitter_language_mapping[inputs.comment])
        parser.set_language(PARSER_LANGUAGE)
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
        sorted_todos = sorted(todos, key=lambda todo: todo.task)  # This simplifies testing
        return Outputs(todos=sorted_todos)


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
