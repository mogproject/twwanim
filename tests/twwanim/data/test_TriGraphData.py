import unittest
from random import Random

import networkx as nx
from twwanim.data.TriGraphData import TriGraphData


class TestTriGraphData(unittest.TestCase):
    """Tests TriGraphData class."""

    def test_contract(self):
        gg = nx.Graph()
        gg.add_edges_from([(1, 2), (1, 3), (2, 3), (2, 4), (3, 5)])

        g = TriGraphData(gg)

        self.assertEqual(g.edge_orientation, {
            (1, 2): (1, 2),
            (2, 1): (1, 2),
            (1, 3): (1, 3),
            (3, 1): (1, 3),
            (2, 3): (2, 3),
            (3, 2): (2, 3),
            (2, 4): (2, 4),
            (4, 2): (2, 4),
            (3, 5): (3, 5),
            (5, 3): (3, 5),
        })

        act = g.contract(4, 1)

        self.assertEqual(act.highlight_to_red, [(1, 3)])
        self.assertEqual(act.highlight_white_to_green, [(1, 2), (2, 4)])
        self.assertEqual(act.highlight_red_to_green, [])
        self.assertEqual(act.edge_shrink, [])
        self.assertEqual(act.edge_move, [(1, 3, 4, 3), (1, 2, 4, 2)])
        self.assertEqual(act.edge_fadeout, [(1, 2)])

        self.assertEqual(g.max_red_degree(), 1)

        act = g.contract(5, 4)

        self.assertEqual(act.highlight_to_red, [(2, 4)])
        self.assertEqual(act.highlight_white_to_green, [(3, 5)])
        self.assertEqual(act.highlight_red_to_green, [(4, 3)])
        self.assertEqual(act.edge_shrink, [])
        self.assertEqual(act.edge_move, [(2, 4, 2, 5), (4, 3, 5, 3)])
        self.assertEqual(act.edge_fadeout, [(3, 5)])

        self.assertEqual(g.max_red_degree(), 2)

        act = g.contract(3, 5)

        self.assertEqual(act.highlight_to_red, [])
        self.assertEqual(act.highlight_white_to_green, [(2, 3)])
        self.assertEqual(act.highlight_red_to_green, [(2, 5)])
        self.assertEqual(act.edge_shrink, [(5, 3, 1)])
        self.assertEqual(act.edge_move, [(2, 5, 2, 3)])
        self.assertEqual(act.edge_fadeout, [(2, 3)])

        self.assertEqual(g.max_red_degree(), 1)

        act = g.contract(2, 3)

        self.assertEqual(act.highlight_to_red, [])
        self.assertEqual(act.highlight_white_to_green, [])
        self.assertEqual(act.highlight_red_to_green, [])
        self.assertEqual(act.edge_shrink, [(2, 3, 0)])
        self.assertEqual(act.edge_move, [])
        self.assertEqual(act.edge_fadeout, [])

        self.assertEqual(g.max_red_degree(), 0)

    def test_contract_random(self):
        rand = Random(12345)
        ns = [10, 100, 200]
        shrink_seen = 0
        for _ in range(3):
            for n in ns:
                for p in [0.1, 0.3, 0.5]:
                    gg = nx.erdos_renyi_graph(n, p)
                    g = TriGraphData(gg.copy())

                    while len(gg) >= 2:
                        u, v = rand.sample(list(gg.nodes()), 2)

                        act = g.contract(u, v)
                        gg.remove_node(v)

                        # check vertices
                        self.assertEqual(set(g.gb.nodes()), set(g.gr.nodes()))

                        # black and red edges must be disjoint
                        self.assertFalse(set(g.gb.edges()) & set(g.gr.edges()))

                        if act.edge_shrink:
                            shrink_seen += 1
                            x, y, z = act.edge_shrink[0]
                            self.assertEqual([x, y][z], u)
                            self.assertEqual([x, y][1 - z], v)
        self.assertGreater(shrink_seen, 1)
