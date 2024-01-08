import os
import argparse
import json
from contextlib import redirect_stdout
from typing import Hashable, Sequence, Tuple

import networkx as nx

with redirect_stdout(open(os.devnull, 'w')):
    # workaround: https://github.com/ManimCommunity/manim/issues/3326
    from manim import tempconfig

from manim import config as globalconfig
from manim._config.utils import _determine_quality

from twwanim.TwinwidthAnimation import TwinwidthAnimation
from twwanim.readwrite import *


def get_parser():
    """Argument parser."""

    version = __import__('twwanim').__version__

    parser = argparse.ArgumentParser(description='Twinwidth animation tools.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version}')
    parser.add_argument('-p', '--preview', action='store_true', help="preview the Scene's animation")
    parser.add_argument('-q', '--quality', default='h', choices=['l', 'm', 'h', 'p', 'k'], help=''.join([
        'Render quality at the follow resolution framerates, respectively: ',
        '854x480 15FPS, 1280x720 30FPS, 1920x1080 60FPS, 2560x1440 60FPS, 3840x2160 60FPS'
    ]))
    parser.add_argument('-s', '--speed', type=float, default=1.0, help='playback speed (default: 1.0)')
    parser.add_argument('--format', default='mp4', choices=['png', 'gif', 'mp4', 'webm', 'mov'], help='output format (default: mp4)')
    parser.add_argument('-r', '--resolution', metavar='W,H', help='resolution in "W,H"')
    parser.add_argument('--fps', '--frame_rate', metavar='FLOAT', type=float, help='render at this frame rate')
    parser.add_argument('graph_path', metavar='GRAPH_PATH', help='path to the input graph file')
    parser.add_argument('cs_path', metavar='CS_PATH', help='path to the input contraction sequence file')

    return parser


def load_graph(path: str) -> nx.Graph:
    if path.endswith('.json'):
        with open(path) as f:
            return nx.node_link_graph(json.load(f))
    elif path.endswith('.gr'):
        return load_pace_2023(path, zero_indexed=False)
    else:
        NotImplementedError('unsupported graph file')


def load_cs(path: str) -> Sequence[Tuple[Hashable, Hashable]]:
    if path.endswith('.json'):
        with open(path) as f:
            return json.load(f)
    else:
        return load_contraction_file(path, zero_indexed=False)


def main(args):
    # load input files
    g = load_graph(args.graph_path)
    cs = load_cs(args.cs_path)

    # test if `pos` is set for all nodes
    if len(nx.get_node_attributes(g, 'pos')) != len(g):
        print(f'Using default graph layout: n={len(g)}, m={g.number_of_edges()}')
        nx.set_node_attributes(g, nx.spring_layout(g), 'pos')

    # call manim's render()
    config = globalconfig.copy()
    try:
        config.quality = _determine_quality(args.quality)
        config.format = args.format
        if args.resolution is not None:
            w, h = map(int, args.resolution.split(','))
            config.pixel_width = w
            config.pixel_height = h
        if args.fps is not None:
            config.frame_rate = args.fps
    except Exception as e:
        raise f'Commandline format error: {e}'

    # render the scene
    with tempconfig(config):
        scene = TwinwidthAnimation()
        scene.set_graph(g)
        scene.set_contraction_sequence(cs)
        scene.set_speed(args.speed)

        try:
            scene.render(args.preview)
        except Exception:
            return 1  # error while rendering


def run_main():
    main(get_parser().parse_args())
