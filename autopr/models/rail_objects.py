from typing import List, ClassVar, Optional

import pydantic

from autopr.models.artifacts import DiffStr


class RailObject(pydantic.BaseModel):
    rail_spec: ClassVar[str]


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

    diff: Optional[DiffStr] = None


class Commit(RailObject):
    # TODO use this instead of Diff, to get a message describing the changes
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


class FileHunk(RailObject):
    rail_spec = """<string
    name="filepath"
    description="The path to the file we are looking at."
    format="filepath"
    on-fail="noop"
/>
<integer
    name="start_line"
    description="The line number of the first line of the hunk."
    format="positive"
    required="false"
    on-fail="noop"
/>
<integer
    name="end_line"
    description="The line number of the last line of the hunk."
    format="positive"
    required="false"
    on-fail="noop"
/>"""

    filepath: str
    start_line: Optional[int] = None
    end_line: Optional[int] = None


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

    def to_str(self):
        return self.commit_message + '\n\n' + self.commit_changes_description


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
    description="The commits that will be made in this pull request. Commits must change the code in the repository, and must not be empty."
>
<object>
{CommitPlan.rail_spec}
</object>
</list>"""

    title: str
    body: str
    commits: list[CommitPlan]

    def to_str(self):
        pr_text_description = f"Title: {self.title}\n\n{self.body}\n\n"
        for i, commit_plan in enumerate(self.commits):
            prefix = f" {' ' * len(str(i + 1))}  "
            changes_prefix = f"\n{prefix}  "
            pr_text_description += (
                f"{str(i + 1)}. Commit: {commit_plan.commit_message}\n"
                f"{prefix}Files: "
                f"{', '.join(commit_plan.relevant_filepaths)}\n"
                f"{prefix}Changes:"
                f"{changes_prefix}{changes_prefix.join(commit_plan.commit_changes_description.splitlines())}\n"
            )
        return pr_text_description
