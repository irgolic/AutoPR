import os
import tempfile
from typing import Optional
from unittest.mock import Mock, MagicMock

from git.repo import Repo
import pytest
from git import GitCommandError

from autopr.services.diff_service import GitApplyService, PatchService
from guardrails.validators import EventDetail
from autopr.validators import create_unidiff_validator


def run_diff_tests_for_file(
    subtests,
    filename: str,
    file_contents: Optional[str],
    file_contents_after: str,
    correct_unidiff: str,
    cases: list[tuple[str, str]]
) -> None:
    # Create temporary directory, put the file in, create a repo
    tmp_dir = tempfile.TemporaryDirectory()
    if file_contents is not None:
        # Create dir if file is in a subdirectory
        dir_name = os.path.dirname(filename)
        if dir_name:
            os.makedirs(os.path.join(tmp_dir.name, dir_name))
        with open(os.path.join(tmp_dir.name, filename), 'w') as f:
            f.write(file_contents)

    repo = Repo.init(tmp_dir.name)

    # Create main branch
    repo.git.checkout('-b', 'main')
    # Create a commit
    if file_contents is not None:
        repo.index.add([filename])
    # Commit, Allow empty
    repo.git.execute(['git', 'commit', '--allow-empty', '-m', 'Initial commit'])
    # Set remote
    # repo.create_remote('origin', '/autopr.git')

    diff_service = PatchService(
        repo=repo,
    )

    validator_class = create_unidiff_validator(repo, diff_service)
    validator = validator_class(on_fail="fix")
    for reason, corrupted_unidiff in cases:
        with subtests.test(msg=reason):
            correct_schema = {"diff": correct_unidiff}
            corrupted_schema = {"diff": corrupted_unidiff}
            error = EventDetail(
                "diff",
                corrupted_unidiff,
                corrupted_schema,
                "",
                None,
            )
            fixed_schema = validator.fix(error)
            assert fixed_schema['diff'] == correct_schema['diff']
            diff_service.apply_diff(fixed_schema['diff'])
            with open(os.path.join(tmp_dir.name, filename), 'r') as f:
                assert f.read() == file_contents_after
        # Git reset hard, clean f
        repo.git.execute(['git', 'reset', '--hard'])
        repo.git.execute(['git', 'clean', '-f'])


def test_unidiff(subtests):
    # Find all test cases in {this_dir}/resources/unidiff
    # Run the test for each file
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_cases_dir = os.path.join(test_dir, 'resources', 'unidiff')
    for test_identifier in os.listdir(test_cases_dir):
        if '%' in test_identifier:
            dir_path_split = test_identifier.split('%')
            filepath = os.path.join(*dir_path_split)
            filename = dir_path_split[-1]
        else:
            filepath = filename = test_identifier
        with subtests.test(filename):
            test_case_dir = os.path.join(test_cases_dir, test_identifier)
            # Assert there is a `correct.diff`
            correct_diff_path = os.path.join(test_case_dir, 'correct.diff')
            assert os.path.exists(correct_diff_path)
            # Assert there is at least one other `.diff` file
            other_diff_names = [
                f for f in os.listdir(test_case_dir)
                if f.endswith('.diff') and f != 'correct.diff'
            ]
            assert len(other_diff_names) > 0
            # Assert there is a file named f"after_{filename}"
            after_file_path = os.path.join(test_case_dir, f"after_{filename}")
            assert os.path.exists(after_file_path)

            # Read the correct diff
            with open(correct_diff_path, 'r') as f:
                correct_unidiff = f.read()
            # Read the file contents after the diff
            with open(after_file_path, 'r') as f:
                file_contents_after = f.read()
            # Read the file contents before the diff (if exists)
            before_file_path = os.path.join(test_case_dir, filename)
            if os.path.exists(before_file_path):
                with open(before_file_path, 'r') as f:
                    file_contents_before = f.read()
            else:
                # If there is no before file, the file is created
                file_contents_before = None
            # Read the other diffs
            other_diffs = []
            for diff_filename in other_diff_names:
                diff_path = os.path.join(test_case_dir, diff_filename)
                with open(diff_path, 'r') as f:
                    other_diffs.append((diff_filename, f.read()))
            run_diff_tests_for_file(
                subtests,
                filepath,
                file_contents_before,
                file_contents_after,
                correct_unidiff,
                other_diffs,
            )
