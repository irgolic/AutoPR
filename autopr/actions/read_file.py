import asyncio
import json
import logging
import os

from pydantic import BaseModel

from autopr.actions.base import Action

logger = logging.getLogger(__name__)


class Inputs(BaseModel):
    filepath: str
    ensure_exists: bool = False


class Outputs(BaseModel):
    contents: str
    success: bool


class ReadFile(Action[Inputs, Outputs]):
    """
    A class representing an action to read the contents of a file.
    """
    id = "read_file"

    @staticmethod
    def load_jupyter_notebook(inputs: Inputs) -> str:
        with open(inputs.filepath) as f:
            data = json.load(f)

        content = ''
        for cell in data['cells']:
            cell_type = cell['cell_type']
            source = ''.join(cell['source'])
            if cell_type == 'markdown':
                content += f'Markdown Cell:\n{source}\n'
            elif cell_type == 'code':
                content += f'Code Cell:\n{source}\n'
                outputs = cell.get('outputs', [])
                for output in outputs:
                    if 'text' in output:
                        content += f'Output:\n{"".join(output["text"])}\n'
        return content

    @staticmethod
    def ensure_file_exists(filepath: str) -> None:
        """
        Ensure that a file exists at the given file path. If the file does not exist,
        create an empty file at that location.
        Args:
            filepath (str): The path to the file to ensure exists.
        Returns:
            None
        """
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write("")

    async def run(self, inputs: Inputs) -> Outputs:
        """Read the contents of a file."""
        if inputs.ensure_exists:
            self.ensure_file_exists(inputs.filepath)
        try:
            if inputs.filepath.endswith('.ipynb'):
                contents = self.load_jupyter_notebook(inputs)
            else:
                with open(inputs.filepath, "r") as f:
                    contents = f.read()
            return Outputs(contents=contents, success=True)
        except Exception as e:
            logger.error(
                f"An unexpected error occurred when reading the file {inputs.filepath}: {e}."
            )
            raise e


if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    filepath = os.path.join(os.getcwd(), "test.txt")
    inputs = Inputs(
        filepath=filepath,
        ensure_exists=True,
    )
    outputs = asyncio.run(run_action_manually(action=ReadFile, inputs=inputs))
    os.remove(filepath)
