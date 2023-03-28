from typing import Optional

from git import Blob
from git.repo import Repo
import pydantic

import structlog

from autopr.utils.tokenizer import get_tokenizer

log = structlog.get_logger()


class FileDescriptor(pydantic.BaseModel):
    path: str
    token_length: int
    chunks: list[list[tuple[int, str]]]  # list of (line number, line content) pairs
    start_chunk: int = 0
    end_chunk: int = -1  # this will be overwritten by the root validator

    @pydantic.root_validator(pre=True)
    def validate_end_chunk(cls, values):
        if 'end_chunk' not in values:
            values['end_chunk'] = len(values['chunks'])
        return values

    def filepaths_with_token_lengths_to_str(self) -> str:
        # TODO give info on what chunks we've already seen
        return f'{self.path} ({str(self.token_length)} tokens)'
        # chunks_left = self.end_chunk - self.start_chunk
        # return f'{self.path} ({str(self.token_length)} tokens) ({str(chunks_left)} chunks left)'

    def filenames_and_contents_to_str(self) -> str:
        contents = ''
        if self.start_chunk > 0:
            contents += f'... #  (omitting {self.start_chunk} chunks)\n'
        # TODO make the line numbers right-aligned with padded spaces,
        #  so that the line numbers don't change the start of the line
        contents += '\n'.join([
            f'{str(line_number)} {line_content}'
            for chunk in self.chunks[self.start_chunk:self.end_chunk]
            for line_number, line_content in chunk
        ])
        if self.end_chunk < len(self.chunks):
            contents += f'\n... #  (omitting {len(self.chunks) - self.end_chunk} chunks)'
        return f'>>> Path: {self.path}:\n\n{contents}'


def trim_chunk(file_desc_with_chunk_start_end: list[FileDescriptor]) -> bool:
    if file_desc_with_chunk_start_end:
        # Find file with most chunks
        longest_num = 0
        longest_i = 0
        for i, desc in enumerate(file_desc_with_chunk_start_end):
            num_chunks = desc.end_chunk - desc.start_chunk
            if num_chunks > longest_num:
                longest_num = num_chunks
                longest_i = i

        desc = file_desc_with_chunk_start_end[longest_i]

        # If we've already looked at the whole file, remove it from the list
        if desc.start_chunk == desc.end_chunk - 1:
            del file_desc_with_chunk_start_end[longest_i]
            return True

        # Otherwise, shave a chunk off the end
        desc.end_chunk -= 1
        file_desc_with_chunk_start_end[longest_i] = desc
        return True
    return False


def filter_seen_chunks(seen_fds: list[FileDescriptor], prospective_fds: list[FileDescriptor]) -> list[FileDescriptor]:
    fds_copy = [f.copy(deep=True) for f in prospective_fds]
    omit_prospective_fd_indices = []
    for selected_fd in seen_fds:
        # If it's in prospective_file_descriptors, update its start_chunk
        for prospective_fd in fds_copy:
            if prospective_fd.path == selected_fd.path:
                # If we've already looked at the whole file, remove it from the list
                if prospective_fd.end_chunk == selected_fd.end_chunk:
                    omit_prospective_fd_indices.append(fds_copy.index(prospective_fd))
                else:
                    prospective_fd.start_chunk = selected_fd.end_chunk
                break
    for i in sorted(omit_prospective_fd_indices, reverse=True):
        del fds_copy[i]
    return fds_copy


_file_descriptor_cache: dict[tuple[bytes, int, int], list[FileDescriptor]] = {}


def repo_to_file_descriptors(repo: Repo, context_window: int, file_chunk_size: int) -> list[FileDescriptor]:
    repo_tree = repo.head.commit.tree

    key = (repo_tree.binsha, context_window, file_chunk_size)
    if key in _file_descriptor_cache:
        return [fd.copy(deep=True) for fd in _file_descriptor_cache[key]]

    file_descriptor_list = []
    for blob in repo_tree.traverse():
        if not isinstance(blob, Blob):
            continue

        if blob.type == 'tree':
            continue
        try:
            content = blob.data_stream.read().decode()
        except UnicodeDecodeError:
            log.debug(f"Error decoding file: {blob.path}")
            continue

        tokenizer = get_tokenizer(context_window)

        tokens = tokenizer.encode(content)
        # Split into chunks up to the last newline
        chunks: list[list[tuple[int, str]]] = []
        line_buffer = []
        for i, line in enumerate(content.splitlines()):
            line_buffer.append((i, line))
            # FIXME speed this up
            token_length = len(tokenizer.encode(
                '\n'.join([l[1] for l in line_buffer])
            ))
            if token_length >= file_chunk_size:
                chunks.append(line_buffer)
                line_buffer = []
        if line_buffer:
            chunks.append(line_buffer)

        token_length = len(tokens)
        file_descriptor_list.append(FileDescriptor(
            path=blob.path,
            token_length=token_length,
            chunks=chunks,
        ))

    _file_descriptor_cache[key] = file_descriptor_list
    return file_descriptor_list
