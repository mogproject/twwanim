[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](http://choosealicense.com/licenses/apache-2.0/) [![PyPI version](https://badge.fury.io/py/twwanim.svg)](http://badge.fury.io/py/twwanim)

# twwanim

**Tw**in-**w**idth **anim**ation tools. Given an (undirected, simple) graph and a corresponding contraction sequence (see [Wikipedia](https://en.wikipedia.org/wiki/Twin-width) for the definition of twin-width), `twwanim` creates a video visualizing contractions and red edges.

![Example](https://github.com/mogproject/twwanim/assets/2019701/c4733c67-e976-4322-9558-4995cbf689b1)

## Dependencies

- [Python 3](https://www.python.org/)
- [LaTeX](https://www.latex-project.org/)
- [Manim Community](https://www.manim.community/) (v0.18.0 or later)
- [NetworkX](https://networkx.org/) (v3.1 or later)

## Installation

- Install LaTeX distribution (the following are recommended):
  - (Mac) [MacTeX](https://tug.org/mactex/): `brew install --cask mactex-no-gui`
  - (Linux) [TeX Live](https://www.tug.org/texlive/):
    - (Debian) `sudo apt install texlive texlive-latex-extra`
    - (Fedora) `sudo dnf install texlive-scheme-full`
  - (Windows) [MikTeX](https://miktex.org/download)
- Install Manim Community: follow the [installation docs](https://docs.manim.community/en/stable/installation.html).
- Install `twwanim`: run `pip install twwanim`.

|Operation|Command|
|:---|:---|
| Install | `pip install twwanim` |
| Upgrade | `pip install --upgrade twwanim` |
| Uninstall | `pip uninstall twwanim` |
| Check installed version | `twwanim --version` |
| Help | `twwanim -h` |

## Getting Started

1. Make sure the command `twwanim` has been installed.

```
$ twwanim --version
twwanim 0.0.1
$ twwanim --help
(the usage will be shown)
```

2. The command `twwanim` takes two inputs: a graph and a contraction sequence.

- Graph file (`.json` or `.gr`):
  - An edge list in the JSON format (output of `json.dumps(networkx.node_link_data(G))`) or the [PACE 2023 input format](https://pacechallenge.org/2023/io/).
  - For the JSON format, you may include the position of each node as a node property `pos`.
  - See the [Jupyter Notebook](https://github.com/mogproject/twwanim/blob/main/notebooks/01_ConvertGraphs.ipynb) for an example of graph conversions.
- Contraction sequence (`.json` or `.txt`):
  - A list of vertex pairs in JSON or in the [PACE 2023 output format](https://pacechallenge.org/2023/io/).

**Example:**

```
twwanim -p -ql tests/resources/pace2023/public/exact_001.json tests/resources/pace2023/public/exact_001_cs.txt
```

- `-p`: Preview the video after rendering it.
- `-ql`: Set the quality to low (854x480 15FPS).
- `tests/resources/pace2023/tiny/tiny001.json`: Path to a graph file.
- `tests/resources/pace2023/tiny/tiny001_cs.txt`: Path to a contraction sequence file.

3. A video will be made in the `media/videos` directory.

The example above will create `media/videos/480p15/TwinwidthAnimation.mp4`.

## Gallery

The following videos are available on YouTube.

- PACE 2023 public instances
  - [exact: 001](https://www.youtube.com/watch?v=OqPAuIvCdao)
  - [exact: 009](https://www.youtube.com/watch?v=Kz7vGT03LnY)
  - [exact: 039](https://www.youtube.com/watch?v=6I1VzQDKT_4)

## Developer's Guide

|Operation|Command|
|:---|:---|
| Run unit tests | `make test` |
| Install in the developer mode | `make dev-install` |
