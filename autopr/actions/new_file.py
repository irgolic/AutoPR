import os
from typing import Optional, Any

from autopr.actions.base import Action, ContextDict
from autopr.actions.utils.file import GeneratedHunkOutputParser, ContextFile, GeneratedFileHunk, make_file_context, \
    add_element_to_context_list

from autopr.actions.utils.commit import CommitPlan
from autopr.models.prompt_chains import PromptChain


class NewFileChain(PromptChain):
    output_parser = GeneratedHunkOutputParser()
    prompt_template = f"""Hey, we've got a new file to create.

{{context}}

This is the codebase subset we decided to look at:
```
{{context_hunks}}
```

This is the plan for the file we're creating:
```
{{plan}}
```

Please send me the contents of the file."""

    context: ContextDict
    context_hunks: list[ContextFile]
    plan: str


class NewFile(Action):
    id = "new_file"
    description = "Make a new file."

    class Arguments(Action.Arguments):
        filepath: str
        description: str

        output_spec = f"""
<string
    name="filepath"
    description="Path to the newly created file."
    required="true"
/>
<string
    name="description"
    description="Description of the contents of the new file."
    required="true"
/>
"""

    def run(
        self,
        args: Arguments,
        context: ContextDict,
    ) -> ContextDict:
        self.publish_service.update_section(title=f"📄 Creating new file: {args.filepath}")

        # Check if file exists
        repo_path = self.repo.working_tree_dir
        assert repo_path is not None
        filepath = os.path.join(repo_path, args.filepath)
        if os.path.exists(filepath):
            self.publish_service.update_section(title=f"❌ Failed to create new file: {args.filepath} "
                                                      f"(file already exists)")
            return add_element_to_context_list(
                context,
                "action_history",
                f"Failed to create new file: {args.filepath} (file already exists)"
            )
        # Check if filename is a directory (doesnt exist yet)
        if os.path.basename(filepath) == "":
            self.publish_service.update_section(title=f"❌ Failed to create new file: {args.filepath} "
                                                      f"(filename is a directory)")
            return add_element_to_context_list(
                context,
                "action_history",
                f"Failed to create new file: {args.filepath} (filename is a directory)"
            )

        # Get the other relevant hunks
        if "current_commit" not in context:
            self.log.error("Context does not specify current_commit")
            context_hunks = []
        elif not isinstance(current_commit := context["current_commit"], CommitPlan):
            self.log.error("Context current_commit is not a CommitPlan")
            context_hunks = []
        else:
            # TODO remove the hunk that's being edited, but leave surrounding context
            #  or rather, build better context by iteratively asking about it
            context_hunks = make_file_context(self.repo, current_commit)

        # Run new file langchain
        new_file_chain = NewFileChain(
            context=context,
            context_hunks=context_hunks,
            plan=args.description,
        )
        new_file_hunk: Optional[GeneratedFileHunk] = self.chain_service.run_chain(new_file_chain)
        if new_file_hunk is None:
            self.publish_service.update_section(title=f"❌ Failed to create new file: {args.filepath}")
            return add_element_to_context_list(
                context,
                "action_history",
                f"Failed to create new file: {args.filepath}"
            )

        # Create dirs
        dirpath = os.path.dirname(filepath)
        os.makedirs(dirpath, exist_ok=True)

        # Write file
        path = os.path.join(repo_path, filepath)
        with open(path, "w") as f:
            f.write(new_file_hunk.contents)

        self.publish_service.update_section(title=f"📄 Created new file: {args.filepath}")
        if outcome := new_file_hunk.outcome:
            outcome = " with outcome: " + outcome
        return add_element_to_context_list(
            context,
            "action_history",
            f"Created {args.filepath}{outcome}"
        )
