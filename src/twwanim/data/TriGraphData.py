import networkx as nx
from typing import Hashable
from twwanim.data.ContractAction import ContractAction

__all__ = ['TriGraphData']

class TriGraphData:
    def __init__(self, g: nx.Graph) -> None:
        self.gb = g  # black graph
        self.gr = nx.empty_graph(g.nodes())  # type: nx.Graph  # red graph
        self.edge_orientation = {}
        for u, v in g.edges():
            self.edge_orientation[u, v] = (u, v)
            self.edge_orientation[v, u] = (u, v)

    def max_red_degree(self) -> int:
        return max(d for _, d in self.gr.degree())

    def contract(self, u: Hashable, v: Hashable) -> ContractAction:
        ret = ContractAction()
        b_u_nbrs = set(self.gb[u])
        b_v_nbrs = set(self.gb[v])
        r_u_nbrs = set(self.gr[u])
        r_v_nbrs = set(self.gr[v])
        o = self.edge_orientation

        # edges between u and v
        if v in (b_u_nbrs | r_u_nbrs):
            ret.edge_shrink += [(u, v, 0) if o[u, v][0] == u else (v, u, 1)]

        # unshared neighbors
        for w in (b_v_nbrs | r_v_nbrs) - b_u_nbrs - r_u_nbrs - {u, v}:
            ret.highlight_to_red += [o[v, w]]

            # Move: vw -> uw
            ret.edge_move += [(v, w, u, w) if o[v, w][0] == v else (w, v, w, u)]

        for w in (b_u_nbrs | r_u_nbrs) - b_v_nbrs - r_v_nbrs - {u, v}:
            ret.highlight_to_red += [o[u, w]]

        # common neighbors
        for w in (b_v_nbrs & (b_u_nbrs | r_u_nbrs)) | (r_v_nbrs & r_u_nbrs):
            ret.edge_move += [(v, w, u, w) if o[v, w][0] == v else (w, v, w, u)]
            ret.edge_fadeout += [o[v, w]]
            if w in b_v_nbrs:
                ret.highlight_white_to_green += [o[v, w]]
            else:
                assert w in r_v_nbrs
                ret.highlight_red_to_green += [o[v, w]]
            if w in b_u_nbrs:
                ret.highlight_white_to_green += [o[u, w]]
            else:
                assert w in r_u_nbrs
                ret.highlight_red_to_green += [o[u, w]]

        for w in r_v_nbrs & b_u_nbrs:
            ret.highlight_red_to_green += [o[v, w]]
            ret.highlight_white_to_green += [o[u, w]]
            ret.edge_move += [(v, w, u, w) if o[v, w][0] == v else (w, v, w, u)]
            ret.edge_fadeout += [o[u, w]]

        # update graph info
        for w in ((b_v_nbrs | r_v_nbrs) - b_u_nbrs - r_u_nbrs - {u, v}) | (r_v_nbrs & b_u_nbrs):
            self.gr.add_edge(u, w)

        for w in b_u_nbrs - (b_v_nbrs | r_v_nbrs) - {v}:
            self.gr.add_edge(u, w)
            self.gb.remove_edge(u, w)

        for w in r_v_nbrs & b_u_nbrs:
            self.gb.remove_edge(u, w)

        self.gb.remove_node(v)
        self.gr.remove_node(v)

        # update edge orientation
        if ret.edge_shrink:
            del self.edge_orientation[u, v]
            del self.edge_orientation[v, u]

        for w in (b_v_nbrs | r_v_nbrs) - {u, v}:
            del self.edge_orientation[v, w]
            del self.edge_orientation[w, v]

        for a, b, c, d in ret.edge_move:
            if (a, b) not in ret.edge_fadeout:
                self.edge_orientation[c, d] = (c, d)
                self.edge_orientation[d, c] = (c, d)

        return ret
