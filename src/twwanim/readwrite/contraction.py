from typing import TextIO

__all__ = ['read_contraction_file', 'load_contraction_file']


def read_contraction_file(input: TextIO, zero_indexed: bool = True) -> list[tuple[int, int]]:
    offset = 1 if zero_indexed else 0
    ret = []

    for line in input.readlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('c'):
            continue  # ignore comments

        u, v = map(int, line.split())
        ret += [(u - offset, v - offset)]
    return ret


def load_contraction_file(path: str, zero_indexed: bool = True) -> list[tuple[int, int]]:
    with open(path) as f:
        return read_contraction_file(f, zero_indexed)
