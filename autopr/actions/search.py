import asyncio
import pydantic
import os
from typing import Optional
from autopr.actions.base import Action

class SearchHit(pydantic.BaseModel):
    filepath: str
    line_number: int
    char_number: int

# The action's inputs
class Inputs(pydantic.BaseModel):
    query: str
    directory_path: Optional[str] = None

# The action's outputs
class Outputs(pydantic.BaseModel):
    hits: list[SearchHit]

async def search_file(filepath: str, query: str, directory_path: str) -> list[SearchHit]:
    hits = []
    try:
        with open(filepath, "r") as f:
            for line_number, line in enumerate(f.readlines()):
                if query in line:
                    hits.append(
                        SearchHit(
                            filepath=os.path.relpath(filepath, start=directory_path),
                            line_number=line_number + 1,
                            char_number=line.index(query),
                        )
                    )
    except Exception as e:
        print(f"An error occurred while processing {filepath}: {e}")
    return hits

class Search(Action[Inputs, Outputs]):
    """
    Search across all files in a directory (and its subdirectories) for a given query.
    """

    id = "search"

    async def run(self, inputs: Inputs) -> Outputs:
        # Get the directory path to search
        directory_path = os.path.join(os.getcwd(), inputs.directory_path) if inputs.directory_path else os.getcwd()

        # Run the search
        hits = []
        for root, dirs, files in os.walk(directory_path):
            if ".git" in dirs:
                dirs.remove(".git")
            if ".git" in files:
                files.remove(".git")
                
            for filename in files:
                filepath = os.path.abspath(os.path.join(root, filename))
                hits += await search_file(filepath, inputs.query, directory_path)

        return Outputs(hits=hits)

# When you run this file
if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    asyncio.run(
        # Run the action manually
        run_action_manually(
            action=Search,
            inputs=Inputs(
                query="TEST",
                directory_path="subfolder",
            ),
            repo_resource="repo_for_searching"
        )
    )