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
