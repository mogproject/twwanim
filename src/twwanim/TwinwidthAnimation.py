import networkx as nx
from manim import *
from typing import Hashable, Sequence, Tuple
from twwanim.TriGraph import TriGraph

__all__ = ['TwinwidthAnimation']


# ===============================================================================
#    Scene
# ===============================================================================
class TwinwidthAnimation(Scene):
    def set_graph(self, graph: nx.Graph) -> None:
        gb = graph.copy()  # black graph
        gr = nx.Graph()
        gr.add_nodes_from(gb.nodes())  # red graph

        # normalize scale
        layout = nx.get_node_attributes(gb, 'pos')
        scale = self._find_scale(layout)

        for k, v in layout.items():
            if len(v) == 2:
                x, y = v
                z = 0.0
            elif len(v) == 3:
                x, y, z = v
            else:
                assert False, 'position must be in 2d or 3d'

            layout[k] = [x * scale, y * scale, z * scale]

        nx.set_node_attributes(gb, layout, 'pos')

        self.gb = gb
        self.gr = gr

    def set_contraction_sequence(self, cs: Sequence[Tuple[Hashable, Hashable]]) -> None:
        self.cs = cs

    def set_speed(self, speed: float) -> None:
        if speed <= 0:
            raise ValueError(f'speed must be a positive number: given {speed}')
        self.speed = 1.0 / speed  # store reciprocal

    def _find_scale(self, layout: dict[Hashable, Sequence[float]]):
        dim = [len(v) for v in layout.values()]

        if all(d == 2 for d in dim):
            is_3d = False
        elif all(d == 3 for d in dim):
            is_3d = True
        else:
            assert False, 'unsupported dimensions'

        min_x = min(v[0] for v in layout.values())
        max_x = max(v[0] for v in layout.values())
        min_y = min(v[1] for v in layout.values())
        max_y = max(v[1] for v in layout.values())
        max_range = max(max_x - min_x, max_y - min_y)

        if is_3d:
            min_z = min(v[2] for v in layout.values())
            max_z = max(v[2] for v in layout.values())
            max_range = max(max_range, max_z - min_z)

        return 6.5 / max_range if max_range > 0 else 1

    def construct(self):
        G = TriGraph(self.gb, LEFT * 2)
        self.play(G.create(), run_time=1)

        tww = 0
        tww_label = Tex('Twin-width:').to_edge(UR).shift(LEFT * 1.5)
        tww_count = MathTex(f'{tww}').next_to(tww_label)

        table_font_size = 28
        table_base_y = 2.5
        row_height = 0.3

        table_header_time = Tex('time', font_size=table_font_size).move_to([2.7, table_base_y + row_height + 0.1, 0.0], aligned_edge=UL)
        table_header_contraction = Tex('contraction', font_size=table_font_size).move_to([3.6, table_base_y + row_height + 0.1, 0.0], aligned_edge=UL)
        table_header_reddeg = Tex('max red deg.', font_size=table_font_size).move_to([5.2, table_base_y + row_height + 0.1, 0.0], aligned_edge=UL)
        tww_line = Line([2.6, 2.6, 0.0], [6.9, 2.6, 0.0], stroke_width=1)

        self.play(
            Succession(
                Write(tww_label),
                FadeIn(tww_count)
            )
        )

        self.play(
            Succession(
                Create(table_header_time),
                Create(table_header_contraction),
                Create(table_header_reddeg),
            ),
            Create(tww_line),
            run_time=0.5
        )

        rows = []
        num_max_rows = 20

        for t, (u, v) in enumerate(self.cs):
            # scroll up
            if len(rows) == num_max_rows:
                self.play(
                    *(FadeOut(x) for x in rows[0]),
                    *(x.animate.shift(row_height * UP) for row in rows[1:] for x in row)
                )
                rows = rows[1:]

            # main transition
            row_y = 2.4 - row_height * len(rows)
            row_time = Tex(f'${t + 1}$', font_size=table_font_size).move_to([3.0, row_y, 0.0], aligned_edge=ORIGIN)
            row_contraction = Tex(f'${u} \gets {v}$', font_size=table_font_size).move_to([4.2, row_y, 0.0], aligned_edge=ORIGIN)

            # Do contraction
            G.contract(self, u, v, [Write(row_time), Write(row_contraction)], self.speed)

            # Update red degrees
            reddeg = G.max_red_degree()
            tww_updated = False
            if tww < reddeg:
                tww = reddeg
                tww_updated = True

            row_reddeg = Tex(f'${reddeg}$', font_size=table_font_size).move_to([6.0, row_y, 0.0], aligned_edge=ORIGIN)
            rows += [[row_time, row_contraction, row_reddeg]]

            if tww_updated:
                tww_count_new = MathTex(f'{tww}').next_to(tww_label, RIGHT)

                self.play(
                    Write(row_reddeg),
                    ReplacementTransform(tww_count, tww_count_new),
                    run_time=1.0 * self.speed
                )
                tww_count = tww_count_new
            else:
                self.play(Write(row_reddeg), run_time=1.0 * self.speed)
