from typing import List, ClassVar

import pydantic


class RailModel(pydantic.BaseModel):
    rail_spec: ClassVar[str] = ...


class Commit(RailModel):
    rail_spec = """<object name="commit">
    <string
        name="message"
        description="The message of the commit."
        required="true"
        format="length: 5 72"
        on-fail-length="noop"
    />
    <string
        name="diff"
        description="The git diff of the commit."
        required="true"
        format="patch"
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
    <url
        name="initial_message"
        description="The first message of the pull request."
        required="true"
        format="valid-url"
        on-fail-valid-url="filter"
    />
    <list name="commits" format="min-len: 1; max-len: 1">
        {Commit.rail_spec}
    </list>
</object>"""

    title: str
    initial_message: str
    commits: List[Commit]
