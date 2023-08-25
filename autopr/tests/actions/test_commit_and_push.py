import pytest
from git.repo import Repo

from autopr.models.executable import ExecutableId
from autopr.tests.utils import create_ephemeral_main_service, run_action_manually_with_main


@pytest.mark.asyncio
async def test_commit_and_push():
    # test action with no inputs
    main_service = create_ephemeral_main_service()
    with open("test.txt", "w") as f:
        f.write("Hello, world!")
    await run_action_manually_with_main(
        main=main_service,
        action=ExecutableId("commit_and_push"),
        inputs={
            "commit_message": "My commit message",
        }
    )

    def check_commit(commit):
        # assert commit message
        assert commit.message == "My commit message\n"
        # assert file was added
        assert commit.stats.files["test.txt"] == {
            "insertions": 1,
            "deletions": 0,
            "lines": 1,
        }

    # verify commit in local repo
    check_commit(main_service.repo.commit())

    # verify commit in remote (bare) repo
    remote_repo_dir = main_service.repo.remote().url
    remote_repo = Repo(remote_repo_dir)
    assert remote_repo.bare
    check_commit(remote_repo.commit("autopr/1"))
