import networkx as nx
from manim import *
from typing import Sequence, Hashable
from twwanim.data.TriGraphData import TriGraphData


class TriGraph:
    def __init__(self, g: nx.Graph, shift: Sequence[float]) -> None:
        n = len(g)
        if n <= 30:
            scale = 1.0
        elif n <= 60:
            scale = 0.9
        elif n <= 80:
            scale = 0.8
        elif n <= 100:
            scale = 0.7
        elif n <= 120:
            scale = 0.6
        else:
            scale = 0.5

        edge_width_normal = 3 * scale
        edge_width_bold = 5 * scale
        edge_opacity_white = 0.7
        edge_opacity_red = 0.95
        vertex_config = dict(radius=0.15 * scale, stroke_width=4 * scale, stroke_color=GRAY_D, z_index=100)
        edge_config = dict(stroke_width=edge_width_normal, stroke_opacity=edge_opacity_white, stroke_color=WHITE, z_index=1)

        G = Graph(
            g.nodes(),
            [],
            labels=True,
            layout=nx.get_node_attributes(g, 'pos'),
            layout_scale=3,
            vertex_config=vertex_config
        ).shift(shift)

        # create mobjects
        edges = {(u, v): Line(G[u].get_center(), G[v].get_center(), **edge_config) for u, v in g.edges()}

        for tex in G._labels.values():
            tex.set_z_index(101)
            tex.font_size = 24 * scale * (0.7 if n >= 100 else 1.0)

        self.g = TriGraphData(g)
        self.G = G
        self.edges = edges
        self.edge_width_normal = edge_width_normal
        self.edge_width_bold = edge_width_bold
        self.edge_opacity_white = edge_opacity_white
        self.edge_opacity_red = edge_opacity_red
        self.vertex_config = vertex_config

    def max_red_degree(self) -> int:
        return self.g.max_red_degree()

    def create(self) -> AnimationGroup:
        return Succession(
            AnimationGroup(Create(self.G), run_time=0.3),
            AnimationGroup(*(Create(self.edges[e]) for e in self.edges), run_time=0.7)
        )

    def contract(
        self,
        scene: Scene,
        u: Hashable,
        v: Hashable,
        extra_animations: Sequence[AnimationGroup],
        animation_speed: float,
    ):
        # -----------------------------------------------------------------------
        # Update inner data structure.
        # -----------------------------------------------------------------------

        act = self.g.contract(u, v)

        # -----------------------------------------------------------------------
        # [Animation 1]: Flash target vertices.
        # -----------------------------------------------------------------------

        scene.play(
            Flash(self.G[u], line_length=0.3),
            Flash(self.G[v], line_length=0.3),
            self.G[u].animate.set_stroke_color(YELLOW),
            self.G[v].animate.set_stroke_color(YELLOW),
            *extra_animations,
            run_time=0.6 * animation_speed
        )

        # -----------------------------------------------------------------------
        # [Animation 2]: Highlight incident edges.
        # -----------------------------------------------------------------------

        if act.highlight_to_red or act.highlight_white_to_green or act.highlight_red_to_green:
            scene.play(
                *(self.edges[e].animate
                  .set_stroke_color(BLUE_C)
                  .set_stroke_width(self.edge_width_bold)
                  .set_opacity(self.edge_opacity_red) for e in act.highlight_red_to_green),
                *(self.edges[e].animate
                  .set_stroke_color(BLUE_C)
                  .set_stroke_width(self.edge_width_bold)
                  .set_opacity(self.edge_opacity_red) for e in act.highlight_white_to_green),
                *(self.edges[e].animate
                  .set_stroke_color(RED_E)
                  .set_stroke_width(self.edge_width_bold)
                  .set_opacity(self.edge_opacity_red) for e in act.highlight_to_red),
                run_time=0.5 * animation_speed
            )
        if act.highlight_white_to_green or act.highlight_red_to_green:
            scene.play(
                *(self.edges[e].animate
                  .set_stroke_color(WHITE)
                  .set_stroke_width(self.edge_width_normal)
                  .set_opacity(self.edge_opacity_white) for e in act.highlight_white_to_green),
                *(self.edges[e].animate
                  .set_stroke_color(RED_E)
                  .set_stroke_width(self.edge_width_normal)
                  .set_opacity(self.edge_opacity_red) for e in act.highlight_red_to_green),
                run_time=0.5 * animation_speed
            )

        # -----------------------------------------------------------------------
        # [Animation 3]: Move merged vertex and its incident edges.
        # -----------------------------------------------------------------------

        scene.play(
            self.G[v].animate.move_to(self.G[u]).set_opacity(0),  # vertex
            *(self.edges[a, b].animate.put_start_and_end_on(  # edges
                self.G[c].get_center(), self.G[d].get_center()
            ) for a, b, c, d in act.edge_move),
            *(self.edges[x, y].animate.put_start_and_end_on(  # edge uv
                self.G[u].get_center() * 0.999 + self.G[v].get_center() * 0.001 if z == 1 else self.G[u].get_center(),
                self.G[u].get_center() * 0.999 + self.G[v].get_center() * 0.001 if z == 0 else self.G[u].get_center()
            ) for x, y, z in act.edge_shrink),
            run_time=0.8 * animation_speed
        )
        self.G.remove_vertices(v)  # should be already transparent

        # -----------------------------------------------------------------------
        # [Animation 4]: Fade out duplicate edges and reset highlights.
        # -----------------------------------------------------------------------

        # remove old vertex and its incident edges
        scene.play(
            *(FadeOut(self.edges[e]) for e in act.edge_fadeout),
            self.G[u].animate.set_stroke_color(self.vertex_config['stroke_color']),
            *(self.edges[e].animate.set_stroke_width(self.edge_width_normal) for e in act.highlight_to_red),
            run_time=0.4 * animation_speed
        )

        # -----------------------------------------------------------------------
        # Maintain edge look-up table.
        # -----------------------------------------------------------------------

        if act.edge_shrink:
            a, b = act.edge_shrink[0][:2]
            del self.edges[a, b]

        for a, b, c, d in act.edge_move:
            if (a, b) not in act.edge_fadeout:
                self.edges[c, d] = self.edges[a, b]
            del self.edges[a, b]
