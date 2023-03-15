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
        description="The git diff between this commit and the previous, without the index line, able to be applied with `git apply`."
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
        description="The body of the initial post of the pull request."
        required="true"
        format="valid-url"
        on-fail-valid-url="filter"
    />
    {Commit.rail_spec}
</object>"""

    title: str
    initial_message: str
    commits: List[Commit]
