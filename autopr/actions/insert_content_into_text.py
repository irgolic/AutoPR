import asyncio
import os
from typing import Any, Optional

from pydantic import BaseModel

from autopr.actions.base import Action


class Inputs(BaseModel):
    # The existing content of the file/text etc.
    existing_content: str

    # The delimiter to insert the content after. Example: <!-- tag -->
    delimiter: str

    # The content to insert
    content_to_add: str


class Outputs(BaseModel):
    # The content of the file after the insertion
    content: str


class InsertContentIntoText(Action[Inputs, Outputs]):
    """
    This action inserts content into a string at a specified delimiter. If the delimiter occurs only once in the string,
    the content is appended to the end of the string with delimiters. If the delimiter occurs two or more times, the
    content is inserted between the last two delimiters.
    """
    id = "insert_content_into_text"

    @staticmethod
    def insert_tag_content_into_string(
        file_content: str, delimiter: str, content: str
    ) -> str:
        delimiter_occurrences = file_content.count(delimiter)
        if delimiter_occurrences <= 1:
            # If there's no delimiter or only one delimiter, append the content at the end with delimiters.
            return file_content + f"\n\n{delimiter}{content}{delimiter}"
        else:
            # If there are two or more delimiters, insert the content between the last two delimiters.
            first_part, last_part = file_content.rsplit(delimiter, 1)
            start_part, middle_part = first_part.rsplit(delimiter, 1)  # throw away the middle part
            return f"{start_part}{delimiter}{content}{delimiter}{last_part}"


    async def run(self, inputs: Inputs) -> Outputs:
        new_content = self.insert_tag_content_into_string(
            inputs.existing_content, inputs.delimiter, inputs.content_to_add
        )
        return Outputs(content=new_content)


if __name__ == "__main__":
    from autopr.tests.utils import run_action_manually

    # Example 1: No delimiters
    inputs = Inputs(
        existing_content="", delimiter="<!-- tag -->", content_to_add="Insert Me"
    )
    outputs = asyncio.run(
        run_action_manually(action=InsertContentIntoText, inputs=inputs)
    )

    # Example 2: Two delimiters
    inputs.existing_content = (
        "\n\n<!-- tag -->This content is going to get replaced<!-- tag -->"
    )
    outputs = asyncio.run(
        run_action_manually(action=InsertContentIntoText, inputs=inputs)
    )
