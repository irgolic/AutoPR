from unittest.mock import Mock, MagicMock

import pytest

from guardrails.validators import EventDetail
from autopr.validators import create_unidiff_validator

dockerfile = """FROM duffn/python-poetry:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git

# Set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the app
ENTRYPOINT ["/entrypoint.sh"]"""
correct_dockerfile_unidiff = """--- Dockerfile
+++ Dockerfile
@@ -5,6 +5,8 @@
 
 # Set up entrypoint
 COPY entrypoint.sh /entrypoint.sh
+
+# Make entrypoint executable
 RUN chmod +x /entrypoint.sh
 
 # Run the app
"""
wrong_line_counts_dockerfile_unidiff = """--- Dockerfile
+++ Dockerfile
@@ -5,505 +5,10 @@
 
 # Set up entrypoint
 COPY entrypoint.sh /entrypoint.sh
+
+# Make entrypoint executable
 RUN chmod +x /entrypoint.sh
 
 # Run the app
"""
wrong_line_numbers_dockerfile_unidiff = """--- Dockerfile
+++ Dockerfile
@@ -6,6 +4,8 @@
 
 # Set up entrypoint
 COPY entrypoint.sh /entrypoint.sh
+
+# Make entrypoint executable
 RUN chmod +x /entrypoint.sh
 
 # Run the app
"""
hallucinated_lines_dockerfile_unidiff = """--- Dockerfile
+++ Dockerfile
@@ -5,6 +5,8 @@
 
 # Set up entrypoint
 COPY entrypoint.sh /entrypoint.sh
 HUHU
+
+# Make entrypoint executable
 RUN chmod +x /entrypoint.sh
 
 # Run the app
 HIHI
 HAHA
"""
a_b_filename_dockerfile_unidiff = """--- a/Dockerfile
+++ b/Dockerfile
@@ -5,6 +5,8 @@
 
 # Set up entrypoint
 COPY entrypoint.sh /entrypoint.sh
+
+# Make entrypoint executable
 RUN chmod +x /entrypoint.sh
 
 # Run the app
"""
plusplusplus_name_is_wrong_dockerfile_unidiff = """--- Dockerfile
+++ Dockerfile_new
@@ -5,6 +5,8 @@
 
 # Set up entrypoint
 COPY entrypoint.sh /entrypoint.sh
+
+# Make entrypoint executable
 RUN chmod +x /entrypoint.sh
 
 # Run the app
"""

readme = """# Pull Request Drafter Github Action

## Environment Variables

- `GITHUB_TOKEN` - The GitHub token to use for the action. This is automatically provided by GitHub, you do not need to create your own token.
"""

correct_readme_unidiff = """--- README.md
+++ README.md
@@ -1,4 +1,20 @@
-# Pull Request Drafter Github Action
+# Automatic Pull Request Github Action 🎉🚀
 
-## Environment Variables
+## Input Variables
+
+The input variables for this Github Action are documented in `action.yml`. They include:
+
+- `github_token`
+- `openai_api_key`
+- `issue_number`
+- `issue_title`
+- `issue_body`
+- `base_branch`
 
+## Guardrails Library
+
+This Github Action utilizes the guardrails library, which can be found in `generation_service.py` and `validators.py`. The library helps in generating and validating pull requests based on the input variables and the codebase.
+
+## Including the Github Action in Your Repository
+
+To include the Automatic Pull Request Github Action in your own repository, add its configuration to your `.github/workflows` directory. Follow the documentation in `action.yml` for further guidance.
"""

wrong_readme_unidiff = """diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1,6 +1,18 @@
-# Pull Request Drafter Github Action
+# Automatic Pull Request Github Action 🎉🚀
 
-## Environment Variables
+## Input Variables
+
+The input variables for this Github Action are documented in `action.yml`. They include:
+
+- `github_token`
+- `openai_api_key`
+- `issue_number`
+- `issue_title`
+- `issue_body`
+- `base_branch`
 
+## Guardrails Library
+
+This Github Action utilizes the guardrails library, which can be found in `generation_service.py` and `validators.py`. The library helps in generating and validating pull requests based on the input variables and the codebase.
+
+## Including the Github Action in Your Repository
+
+To include the Automatic Pull Request Github Action in your own repository, add its configuration to your `.github/workflows` directory. Follow the documentation in `action.yml` for further guidance.
"""

new_file_unidiff = """--- /dev/null
+++ README.md
@@ -0,0 +1,4 @@
+# Pull Request Drafter Github Action
+
+## Environment Variables
+ 
"""
missing_minusminusminus_unidiff = """+++ README.md
@@ -0,0 +1,4 @@
+# Pull Request Drafter Github Action
+
+## Environment Variables
+ 
"""


@pytest.mark.parametrize(
    "file_contents, correct_unidiff, cases",
    [
        (
            dockerfile,
            correct_dockerfile_unidiff,
            [
                (
                    "Unidiff line counts are wrong",
                    wrong_line_counts_dockerfile_unidiff,
                ),
                (
                    "Unidiff line numbers are wrong",
                    wrong_line_numbers_dockerfile_unidiff,
                ),
                (
                    "Unidiff contains hallucinated lines",
                    hallucinated_lines_dockerfile_unidiff,
                ),
                (
                    "Unidiff contains a/b filenames",
                    a_b_filename_dockerfile_unidiff,
                ),
                (
                    "+++ name is wrong",
                    plusplusplus_name_is_wrong_dockerfile_unidiff,
                ),
            ],
        ),
        (
            readme,
            correct_readme_unidiff,
            [
                (
                    "Unidiff contains git --diff line",
                    wrong_readme_unidiff,
                ),
            ],
        ),
        (
            "",
            new_file_unidiff,
            [
                (
                    "Unidiff is missing ---",
                    missing_minusminusminus_unidiff,
                ),
            ],
        ),
    ],
)
def test_unidiff_fix(subtests, file_contents: str, correct_unidiff: str, cases: list[tuple[str, str]]) -> None:
    """Test that the unidiff_fix function fixes unidiffs."""
    mock_repo = MagicMock()
    mock_tree = MagicMock()
    mock_blob = MagicMock()
    mock_blob.data_stream.read.return_value = file_contents.encode()
    mock_tree.__truediv__.return_value = mock_blob
    validator_class = create_unidiff_validator(mock_repo, mock_tree)
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
