import os
import re
from typing import Optional

from autopr.actions.base import Action, ContextDict
from autopr.actions.new_file import NewFile
from autopr.actions.utils.commit import CommitPlan
from autopr.actions.utils.file import add_element_to_context_list, GeneratedHunkOutputParser, ContextFile, \
    ContextCodeHunk, make_file_context, GeneratedFileHunk
from autopr.models.prompt_chains import PromptChain


class RewriteCodeHunkChain(PromptChain):
    output_parser = GeneratedHunkOutputParser()
    prompt_template = f"""Hey, we've got a new code hunk to diff.

{{context}}

This is the codebase subset we decided to look at:
```
{{context_hunks}}
```

This is the hunk we're rewriting:
```
{{hunk_contents}}
```

This is the plan for how we want to rewrite the hunk:
```
{{plan}}
```

Please rewrite the hunk to match the plan, but do not include any lines prefixed with | in the result.

RULES:
- ONLY rewrite the lines prefixed with *, 
- submit only the lines without the * prefix,
- do not preserve the relative leading indentation of the lines (start the hunk's indentation at 0).

{{format_instructions}}"""

    context: ContextDict
    context_hunks: list[ContextFile]
    hunk_contents: ContextCodeHunk
    plan: str


class EditFile(Action):
    id = "edit_file"
    description = "Rewrite a code hunk in a file."

    class Arguments(Action.Arguments):
        filepath: str
        description: str
        start_line: Optional[int] = None
        end_line: Optional[int] = None

        output_spec = f"""
<string
    name="filepath"
    description="Path to the file to be edited."
    required="true"
/>
<string
    name="description"
    description="Description of the changes to be made to the file."
    required="true"
/>
<integer
    name="start_line"
    description="The line number of the first line of the hunk to be edited."
    format="positive"
    required="false"
    on-fail="noop"
/>
<integer
    name="end_line"
    description="The line number of the last line of the hunk to be edited. Keep the hunk as short as possible while fulfilling the description."
    format="positive"
    required="false"
    on-fail="noop"
/>
"""

    def __init__(
        self,
        *args,
        num_context_lines: int = 3,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        # num_context_lines is the number of lines of context to show around the hunk being edited
        self.num_context_lines = num_context_lines

    @staticmethod
    def _split_into_lines(text: str) -> list[str]:
        lines = text.splitlines()
        # If text ends with a newline, we want to keep that as a line
        if text.rstrip() != text:
            lines.append("")
        return lines

    def run(
        self,
        args: Arguments,
        context: ContextDict,
    ) -> ContextDict:
        # Check if file exists
        repo_path = self.repo.working_tree_dir
        assert repo_path
        filepath = os.path.join(repo_path, args.filepath)
        if not os.path.exists(filepath):
            create_file_action = NewFile(
                repo=self.repo,
                rail_service=self.rail_service,
                chain_service=self.chain_service,
                publish_service=self.publish_service,
            )
            create_args = NewFile.Arguments(
                filepath=args.filepath,
                description=args.description,
            )
            self.log.warning(f"File {filepath} does not exist, creating it instead.")
            return create_file_action.run(create_args, context)

        self.publish_service.update_section(title=f"✍️ Editing file: {args.filepath}")

        # Grab file contents
        with open(filepath, "r") as f:
            lines = self._split_into_lines(f.read())

        # Get relevant hunk
        start_line, end_line = args.start_line, args.end_line
        if not lines:
            code_hunk = ContextCodeHunk(
                code_hunk=[],
            )
            indent = 0
        elif start_line is None or end_line is None:
            line_nums = list(range(1, len(lines) + 1))
            code_hunk = ContextCodeHunk(
                code_hunk=list(zip(line_nums, lines)),
                highlight_line_numbers=line_nums,
            )
            indent = 0
        else:
            # Limit line numbers
            start_line, end_line = min(max(start_line, 1), len(lines)), min(max(end_line, 1), len(lines))
            end_line = max(start_line, end_line)

            code_hunk_lines: list[tuple[int, str]] = []
            context_start_line = max(1, start_line - self.num_context_lines)
            context_end_line = min(len(lines), end_line + self.num_context_lines)
            for line_num in range(context_start_line, context_end_line + 1):
                code_hunk_lines.append((line_num, lines[line_num - 1]))
            highlight_line_nums = list(range(start_line, end_line + 1))
            code_hunk = ContextCodeHunk(
                code_hunk=code_hunk_lines,
                highlight_line_numbers=highlight_line_nums,
            )

            # Find the indentation common to all highlighted lines in the hunk
            highlighted_lines = [
                lines[line_num - 1]
                for line_num in highlight_line_nums
            ]
            lines_for_indent = [
                len(line) - len(line.lstrip())
                for line in highlighted_lines
                if line.strip()
            ]
            if not lines_for_indent:
                indent = 0
            else:
                indent = min(lines_for_indent)

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

        # Run edit file langchain
        edit_file_chain = RewriteCodeHunkChain(
            context=context,
            context_hunks=context_hunks,
            hunk_contents=code_hunk,
            plan=args.description,
        )
        edit_file_hunk: Optional[GeneratedFileHunk] = self.chain_service.run_chain(edit_file_chain)
        if edit_file_hunk is None:
            self.publish_service.update_section(title=f"❌ Failed to edit file: {args.filepath}")
            return add_element_to_context_list(
                context,
                "action_history",
                f"Failed to edit file {args.filepath}",
            )

        new_lines = edit_file_hunk.contents
        # if all lines start with "<int> | " or "<int> * "
        if all(re.match(r"^\s*\d+\s*[|*]\s*", line)
               for line in new_lines.splitlines()):
            # Remove the prefix from all lines
            new_lines = "\n".join(
                re.sub(r"^\s*\d+\s*[|*]\s*", "", line)
                for line in new_lines.splitlines()
            )

        # Add indentation to new lines
        indented_lines = []
        for line in self._split_into_lines(new_lines):
            if not line.strip():
                indented_lines.append("")
                continue
            indented_lines.append(" " * indent + line)

        # Replace lines in file
        if start_line is not None and end_line is not None:
            lines = lines[:start_line - 1] + indented_lines + lines[end_line:]
        else:
            lines = indented_lines

        # Write file
        path = os.path.join(repo_path, filepath)
        with open(path, "w") as f:
            f.write("\n".join(lines))

        self.publish_service.update_section(title=f"✍️ Edited file: {args.filepath}")
        return add_element_to_context_list(
            context,
            "action_history",
            f"Edited file, with outcome: {edit_file_hunk.outcome}"
        )
