import asyncio
import re
from autopr.actions.base import Action
from pydantic import BaseModel
import os

ignore_patterns = [
    r"\.DS_Store$",
    r"Thumbs\.db$",
    r"\.log$",
    r"\.bak$",
    r"\.tmp$",
    r"\.swp$",
    r"\.gitignore$",
    r"\.npmignore$",
    r"\.gitattributes$",
    r"\.env$",
    r"\.classpath$",
    r"\.project$",
    r"\.pytest_cache$",
    r"\.git/",
    r"\.svn/?",
    r"node_modules/?",
    r"__pycache__/?",
    r"\.idea/?",
    r"\.vscode/?",
    r"\.hg/?",
    r"\.dockerignore/?",
    r"\.settings/?",
    r"bin/?",
    r"build/?",
    r"dist/?",
    r"out/?",
    r".*\.egg-info/?",
    r".*\.dist-info/?",
]

IGNORE_PATTERN = re.compile("|".join(ignore_patterns))


class Inputs(BaseModel):
    # Files and subfolders to ignore during the crawl
    entries_to_ignore: list[str] = []

    # The folder to crawl
    folder_path: str = "."

    # Whether to ignore binary files
    ignore_binary_files: bool = True


class Outputs(BaseModel):
    # The files in the folder and subfolders
    contents: list[str]


class WalkFiles(Action[Inputs, Outputs]):
    """
    This action lists all the files and subfolders in a folder, excluding certain files and directories.
    """

    id = "walk_files"

    @staticmethod
    def is_binary(path):
        return b"\x00" in open(path, "rb").read(1024)

    async def run(self, inputs: Inputs) -> Outputs:
        file_entries_to_return = []

        for root, dirs, files in os.walk(inputs.folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                full_path = os.path.normpath(full_path)

                if inputs.ignore_binary_files and self.is_binary(full_path):
                    continue
                if IGNORE_PATTERN.match(full_path):
                    continue
                file_entries_to_return.append(full_path)

        return Outputs(contents=file_entries_to_return)


if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    asyncio.run(
        # Run the action manually
        run_action_manually(
            action=WalkFiles,
            inputs=Inputs(folder_path=os.path.join(os.getcwd(), "..")),
        )
    )
