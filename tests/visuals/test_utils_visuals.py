import unittest
from autolang.visuals.utils_visuals import (eps,
                                            get_edge_label,
                                            get_edge_label_pda,
                                            get_edge_label_tm)

class TestEps(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(eps(''), 'ε')

    def test_nonempty(self):
        self.assertEqual(eps('a'), 'a')


class TestGetEdgeLabel(unittest.TestCase):

    pass


class TestGetEdgeLabelPDA(unittest.TestCase):

    pass


class TestGetEdgeLabelTM(unittest.TestCase):

    pass