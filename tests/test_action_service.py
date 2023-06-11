import unittest
from unittest.mock import patch
from autopr.agents.plan_and_code import PlanAndCode
from autopr.services.action_service import ActionService


class TestActionServiceRestrictCodeChanges(unittest.TestCase):
    def setUp(self):
        self.plan_and_code_agent = PlanAndCode()
        self.action_service = ActionService()

    @patch('autopr.services.action_service.ActionService._write_action_selection_rail_spec')
    def test_restrict_code_changes(self, mock_write_action_selection_rail_spec):
        # Setup a sample PR plan with two commits
        pr_plan = [
            {"title": "Commit 1", "changes": ["Change 1.1", "Change 1.2"]},
            {"title": "Commit 2", "changes": ["Change 2.1", "Change 2.2"]},
        ]

        # Generate the code for the first commit
        self.plan_and_code_agent.write_commit(pr_plan, 0)
        mock_write_action_selection_rail_spec.assert_called_with("Current Commit: Commit 1", [])

        # Generate the code for the second commit
        self.plan_and_code_agent.write_commit(pr_plan, 1)
        mock_write_action_selection_rail_spec.assert_called_with("Current Commit: Commit 2", [])

if __name__ == "__main__":
    unittest.main()