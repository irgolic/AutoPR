import asyncio
import re
from autopr.actions.base import Action
from pydantic import BaseModel
import os

file_patterns = [
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
]

NON_INFORMATIVE_FILES = re.compile("|".join(file_patterns))

dir_patterns = [
    r"\.git/?",
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

NON_INFORMATIVE_DIRECTORIES = re.compile("|".join(dir_patterns))


class Inputs(BaseModel):
    # Files and subfolders to ignore during the crawl
    entries_to_ignore: list[str] = []

    # The folder to crawl
    folder_path: str

    # Whether to ignore binary files
    ignore_binary_files: bool = True


class Outputs(BaseModel):
    # The contents of the folder
    contents: list[str]
    # The url of the crawled folder
    url: str


class ListFolder(Action[Inputs, Outputs]):
    """
    This action lists all the files and subfolders in a folder, excluding certain files and directories.
    """

    id = "list_folder"

    @staticmethod
    def is_binary(path):
        return b"\x00" in open(path, "rb").read(1024)

    async def run(self, inputs: Inputs) -> Outputs:
        all_file_entries = os.listdir(inputs.folder_path) or []
        file_entries_to_return = []

        for el in sorted(all_file_entries):
            full_path = os.path.join(inputs.folder_path, el)

            if el in inputs.entries_to_ignore:
                continue
            if os.path.isfile(full_path) and self.is_binary(full_path):
                continue
            if NON_INFORMATIVE_FILES.match(el):
                continue
            if NON_INFORMATIVE_DIRECTORIES.match(el):
                continue

            file_entries_to_return.append(el)

        url = await self.platform_service.get_file_url(
            inputs.folder_path, self.publish_service.base_branch
        )
        return Outputs(contents=file_entries_to_return, url=url)


if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    asyncio.run(
        # Run the action manually
        run_action_manually(
            action=ListFolder,
            inputs=Inputs(folder_path=os.path.join(os.getcwd(), "..")),
        )
    )
