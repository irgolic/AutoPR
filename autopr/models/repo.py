import pydantic


class RepoCommit(pydantic.BaseModel):
    message: str
    diff: str


class RepoPullRequest(pydantic.BaseModel):
    title: str
    body: str
    commits: list[RepoCommit]
