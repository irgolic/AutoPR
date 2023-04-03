from collections import defaultdict
from typing import Optional

import pydantic
from git import Repo, Tree

from autopr.agents.codegen_agent import CodegenAgentBase
from autopr.models.artifacts import Issue, DiffStr
from autopr.models.prompt_rails import PromptRail
from autopr.models.rail_objects import PullRequestDescription, CommitPlan, RailObject, FileHunk





