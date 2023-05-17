from autopr.actions.action import Action

class DeleteFile(Action):
    def __init__(self, file_path):
        self.file_path = file_path

    def run(self, repository, commit_plan):
        repository.remove_file(self.file_path)
        commit_plan.add_change("delete", self.file_path)