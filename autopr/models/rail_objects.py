from typing import List, ClassVar, Optional

import pydantic


class RailObject(pydantic.BaseModel):
    rail_spec: ClassVar[str] = ...


class InitialFileSelectResponse(RailObject):
    rail_spec = """<list name="filepaths">
    <string
        description="Files in this repository that we should look at."
        format="filepath"
        on-fail="noop"
    />
</list>"""

    filepaths: List[str]


class LookAtFilesResponse(RailObject):
    rail_spec = """<string 
    name="notes" 
    description="Notes relevant to solving the issue, that we will use to plan our code commits." 
    length="1 1000"
    on-fail="noop" 
/>
<list name="filepaths_we_should_look_at">
    <string
        description="The paths to files we should look at next in the repo. Drop any files that are a waste of time with regard to the issue."
        format="filepath"
        on-fail="noop"
    />
</list>"""

    filepaths_we_should_look_at: Optional[List[str]] = None
    notes: str


class Diff(RailObject):
    rail_spec = """<string
    name="diff"
    description="The diff of the commit, in unified format (unidiff), as output by `diff -u`. Changes shown in hunk format, with headers akin to `--- filename\n+++ filename\n@@ .,. @@`."
    required="false"
    format="unidiff"
/>"""

    diff: Optional[str] = None


class Commit(RailObject):
    rail_spec = f"""{Diff.rail_spec}
<string
    name="message"
    description="The commit message, describing the changes."
    required="true"
    format="length: 5 72"
    on-fail-length="noop"
/>"""

    diff: Diff
    commit_message: str


class CommitPlan(RailObject):
    rail_spec = f"""<string
    name="commit_message"
    description="The commit message, concisely describing the changes made."
    length="1 100"
    on-fail="noop"
/>
<list
    name="relevant_filepaths"
    description="The files we should be looking at while writing this commit."
>
    <string
        description="A file path, relative to the root of the repository."
        format="filepath"
        on-fail="fix"
    />
</list>
<string
    name="commit_changes_description"
    description="A description of the changes made in this commit, in the form of a list of bullet points."
    length="1 1000"
    on-fail="noop"
/>"""

    commit_message: str
    relevant_filepaths: List[str] = pydantic.Field(default_factory=list)
    commit_changes_description: str


class PullRequestDescription(RailObject):
    rail_spec = f"""<string 
    name="title" 
    description="The title of the pull request."
/>
<string 
    name="body" 
    description="The body of the pull request."
/>
<list 
    name="commits"
    on-fail="reask"
>
<object>
{CommitPlan.rail_spec}
</object>
</list>"""

    title: str
    body: str
    commits: list[CommitPlan]
