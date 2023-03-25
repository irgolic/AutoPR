from typing import List, ClassVar, Optional, Literal

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


class DiffLine(RailObject):
    rail_spec = """<string
    name="role"
    description="Role of this code line: a (added), r (removed), or u (unchanged)."
    required="true"
    format="valid-choices: a,r,u"
    on-fail-valid-choices="reask"
/>
<integer
    name="indent_spaces"
    description="The number of space characters used for indentation."
    required="true"
    format="valid-range: 0"
    on-fail-valid-range="reask"
/>
<string
    name="content"
    description="Content of the code line, stripped of leading + or - for added and removed lines, and any leading whitespace."
    required="true"
    format="no-leading-whitespace"
    on-fail-no-leading-whitespace="fix"
/>"""

    role: Literal["a", "r", "u"]
    indent_spaces: int
    content: str

    def to_str(self):
        charmap = {
            "a": "+",
            "r": "-",
            "u": " ",
        }
        return f"{charmap[self.role]}{' ' * self.indent_spaces}{self.content}"


class DiffHunk(RailObject):
    rail_spec = f"""<string
    name="file"
    description="Path to the changed file."
    required="true"
/>
<bool
    name="new_file"
    description="Whether this hunk creates a new file."
    required="true"
/>
<integer
    name="start_line"
    description="Line number of the first code line in this hunk."
    required="true"
/>
<list
    name="lines"
    description="List of lines of code in the hunk."
    required="true"
    format="length: 1 100"
    on-fail-length="noop"
>
<object>
{DiffLine.rail_spec}
</object>
</list>"""

    file: str
    new_file: bool
    start_line: int = 1
    lines: List[DiffLine]

    def to_str(self):
        add_count = 0
        remove_count = 0
        for line in self.lines:
            if line.role == "a":
                add_count += 1
            elif line.role == "r":
                remove_count += 1
            else:  # if line.role == "u":
                add_count += 1
                remove_count += 1
        return "\n".join([
            f"--- {self.file}" if not self.new_file else f"--- /dev/null",
            f"+++ {self.file}",
            f"@@ -{self.start_line},{remove_count} +{self.start_line},{add_count} @@"
        ] + [line.to_str() for line in self.lines])


class Diff(RailObject):
    rail_spec = f"""<list
    name="hunks"
    description="List of hunks of code changes."
    required="true"
    format="unidiff"
>
<object>
{DiffHunk.rail_spec}
</object>
</list>"""

    hunks: List[DiffHunk]

    def to_str(self):
        return "\n".join([
            hunk.to_str()
            for hunk in self.hunks
        ] + [""])


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
    description="The commits that will be made in this pull request. Commits must change the code in the repository, and must not be empty."
>
<object>
{CommitPlan.rail_spec}
</object>
</list>"""

    title: str
    body: str
    commits: list[CommitPlan]
