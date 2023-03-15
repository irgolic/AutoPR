from typing import List, ClassVar

import pydantic


class RailModel(pydantic.BaseModel):
    rail_spec: ClassVar[str] = ...


class Commit(RailModel):
    rail_spec = """<object name="commit">
<string
    name="message"
    description="The commit message, describing the changes."
    required="true"
    format="length: 5 72"
    on-fail-length="noop"
/>
<string
    name="diff"
    description="Difference before and after the commit is applied, in unified format (unidiff), as output by `diff -u file1 file2`."
    required="true"
    format="unidiff"
    on-fail-unidiff="reask"
/>
</object>"""

    message: str
    diff: str


class PullRequest(RailModel):
    rail_spec = f"""<object name="pull_request">
<string
    name="title"
    description="The title of the pull request."
    required="true"
    format="length: 10 200"
    on-fail-length="noop"
/>
<string
    name="initial_message"
    description="The body of the initial post of the pull request. Should include a description of the changes in pseudocode, and a link to the issue."
    required="true"
    format="length: 10 2000"
/>
<list name="commits" required="true" filter="length 1">
{Commit.rail_spec}
</list>
</object>"""

    title: str
    initial_message: str
    commits: List[Commit]
