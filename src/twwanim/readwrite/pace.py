import networkx as nx
from typing import TextIO

__all__ = [
    'read_pace_2023',
    'load_pace_2023',
    'write_pace_2023',
    'save_pace_2023',
    'read_pace_2016',
    'load_pace_2016',
    'write_pace_2016',
    'save_pace_2016',
]


def read_pace(input: TextIO, zero_indexed: bool = True) -> nx.Graph:
    offset = 1 if zero_indexed else 0
    G = None
    for line in input.readlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('c'):
            continue  # ignore comments

        if line.startswith('p'):
            _, _, nn, mm = line.split()
            n, m = int(nn), int(mm)
            G = nx.empty_graph(range((1 - offset), (1 - offset) + n))
        else:
            u, v = map(int, line.split())
            assert G is not None
            G.add_edge(u - offset, v - offset)

    assert G is not None
    assert m == G.number_of_edges(), 'inconsistent edges'
    return G


def read_pace_2016(input: TextIO, zero_indexed: bool = True) -> nx.Graph:
    return read_pace(input, zero_indexed)


def read_pace_2023(input: TextIO, zero_indexed: bool = True) -> nx.Graph:
    return read_pace(input, zero_indexed)


def load_pace_2016(path: str, zero_indexed: bool = True) -> nx.Graph:
    with open(path) as f:
        return read_pace_2016(f, zero_indexed)


def load_pace_2023(path: str, zero_indexed: bool = True) -> nx.Graph:
    with open(path) as f:
        return read_pace_2023(f, zero_indexed)


def write_pace(output: TextIO, G: nx.Graph, problem_name: str, comments: list[str] = [], zero_indexed: bool = True) -> None:
    offset = 1 if zero_indexed else 0
    n = G.number_of_nodes()
    m = G.number_of_edges()
    assert set(G.nodes()) == set(range(n))  # labeled [0,n)

    for comment in comments:
        output.write(f'c {comment}\n')

    output.write(f'p {problem_name} {n} {m}\n')
    for u, v in G.edges():
        output.write(f'{u + offset} {v + offset}\n')


def write_pace_2016(output: TextIO, G: nx.Graph, comments: list[str] = [], zero_indexed: bool = True) -> None:
    write_pace(output, G, 'tw', comments, zero_indexed)


def write_pace_2023(output: TextIO, G: nx.Graph, comments: list[str] = [], zero_indexed: bool = True) -> None:
    write_pace(output, G, 'tww', comments, zero_indexed)


def save_pace_2016(path: str, G: nx.Graph, comments: list[str] = [], zero_indexed: bool = True) -> None:
    with open(path, 'w') as f:
        write_pace_2016(f, G, comments, zero_indexed)


def save_pace_2023(path: str, G: nx.Graph, comments: list[str] = [], zero_indexed: bool = True) -> None:
    with open(path, 'w') as f:
        write_pace_2023(f, G, comments, zero_indexed)
