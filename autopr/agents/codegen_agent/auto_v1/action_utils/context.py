import pydantic


class ContextCodeHunk(pydantic.BaseModel):
    """
    A hunk of code that is part of the context for code generation.
    """
    highlight_line_numbers: list[int] = pydantic.Field(default_factory=list)
    code_hunk: list[tuple[int, str]]

    def __str__(self):
        if not self.code_hunk:
            return ''
        max_line_num_width = len(str(self.code_hunk[-1][0]))
        lines = []
        for num, line_content in self.code_hunk:
            num_width = len(str(num))
            line = ' ' * (max_line_num_width - num_width) + str(num)
            if num in self.highlight_line_numbers:
                line += ' * '
            else:
                line += ' | '
            line += line_content
            lines.append(line)
        return '\n'.join(lines)


class ContextFile(pydantic.BaseModel):
    """
    A file that is part of the context for code generation.
    """
    filepath: str
    code_hunks: list[ContextCodeHunk]

    def __str__(self):
        code_hunks_s = '\n\n'.join(
            [str(code_hunk) for code_hunk in self.code_hunks]
        )
        return f">>> File: {self.filepath}\n\n" + code_hunks_s
