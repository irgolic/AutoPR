import unittest
from autopr.agents.plan_and_code import PlanAndCode
from autopr.services.action_service import ActionService


class TestRestrictCodeChanges(unittest.TestCase):
    def setUp(self):
        self.plan_and_code_agent = PlanAndCode()
        self.action_service = ActionService()

    def test_restrict_code_changes(self):
        # Setup a sample PR plan with two commits
        pr_plan = [
            {"title": "Commit 1", "changes": ["Change 1.1", "Change 1.2"]},
            {"title": "Commit 2", "changes": ["Change 2.1", "Change 2.2"]},
        ]

        # Generate the code for the first commit
        code = self.plan_and_code_agent.write_commit(
            pr_plan, 0, context_headings=["Current Commit: Commit 1"]
        )

        # Check if the generated code only contains changes related to the first commit
        self.assertIn("Change 1.1", code)
        self.assertIn("Change 1.2", code)
        self.assertNotIn("Change 2.1", code)
        self.assertNotIn("Change 2.2", code)

        # Generate the code for the second commit
        code = self.plan_and_code_agent.write_commit(
            pr_plan, 1, context_headings=["Current Commit: Commit 2"]
        )

        # Check if the generated code only contains changes related to the second commit
        self.assertNotIn("Change 1.1", code)
        self.assertNotIn("Change 1.2", code)
        self.assertIn("Change 2.1", code)
        self.assertIn("Change 2.2", code)


if __name__ == "__main__":
    unittest.main()