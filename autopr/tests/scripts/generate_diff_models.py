import os
import json
import tempfile
import threading

import git

from autopr.models.rail_objects import Diff
from autopr.models.rails import NewDiff
from autopr.services.diff_service import PatchService
from autopr.services.rail_service import RailService
from autopr.validators import create_unidiff_validator


def process_diff_file(diff_path, rail_service):
    print(f'Processing {diff_path}...')
    json_path = os.path.join(os.path.dirname(diff_path), f'{os.path.basename(diff_path)}.json')
    # If json file already exists, skip
    if os.path.exists(json_path):
        return

    # Read diff file
    with open(diff_path, 'r') as f:
        diff = f.read()

    # Run rail over the diff file and save dict output
    raw_o, dict_o = rail_service._run_rail(NewDiff, diff)
    with open(json_path, 'w') as f:
        json.dump(json.loads(raw_o), f, indent=4)
    print(f'Processed {diff_path}!')


def main():
    # Load diff files from ../resources/unidiff
    path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'unidiff')
    path = os.path.normpath(path)

    # Create temporary directory, put the files in
    tmp_dir = tempfile.TemporaryDirectory()
    # For each folder in ../resources/unidiff, create a file
    for dirname in os.listdir(path):
        if '%' in dirname:
            filepath = dirname.replace('%', '/')
            filename = filepath.split('/')[-1]
            dirname_stem = os.path.dirname(filepath)

            # Create dir if file is in a subdirectory
            tmpdir_dirpath = os.path.join(tmp_dir.name, dirname_stem)
            os.makedirs(tmpdir_dirpath, exist_ok=True)
            tmpdir_filepath = os.path.join(tmpdir_dirpath, filename)
        else:
            filename = dirname
            tmpdir_filepath = os.path.join(tmp_dir.name, dirname)
        # Copy nested file with same name as filename
        resource_filepath = os.path.join(path, dirname, filename)
        if os.path.exists(resource_filepath):
            with open(resource_filepath, 'r') as f:
                file_contents = f.read()
            with open(tmpdir_filepath, 'w') as f:
                f.write(file_contents)

    # Init repo
    repo = git.Repo.init(tmp_dir.name)
    # Create main branch
    repo.git.checkout('-b', 'main')
    # Create a commit
    repo.git.execute(['git', 'add', '-A'])
    # Commit, Allow empty
    repo.git.execute(['git', 'commit', '--allow-empty', '-m', 'Initial commit'])

    # For each diff in ../resources/unidiff (recursively), generate a `.diff.json` file
    # that reflects the structure in the Diff model
    rail_service = RailService(
        completion_model='gpt-4',
    )
    diff_service = PatchService(
        repo=repo,
    )

    # Create guardrails validator
    create_unidiff_validator(repo, diff_service)

    threads = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith('.diff'):
                diff_path = os.path.join(root, filename)
                t = threading.Thread(target=process_diff_file, args=(diff_path, rail_service))
                threads.append(t)
                t.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
