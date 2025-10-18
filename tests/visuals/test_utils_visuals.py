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

    def test_single_letter(self):
        self.assertEqual(get_edge_label(['a']), 'a')
        self.assertEqual(get_edge_label(['']),  'ε')

    def test_multiple_letters(self):
        # High max length to prevent abbreviation
        self.assertEqual(get_edge_label(['a','b'], max_length=100),         'a,b')
        self.assertEqual(get_edge_label(['a','b','c'], max_length=100),     'a,b,c')
        self.assertEqual(get_edge_label(['a','b','c','d'], max_length=100), 'a,b,c,d')

    def test_abbreviate(self):
        # Low max length to ensure abbreviation
        self.assertEqual(get_edge_label(['aaaaaaaa'], max_length=1),      'aaaaaaaa')
        self.assertEqual(get_edge_label(['a','b','c'], max_length=1),     'a,…,c')
        self.assertEqual(get_edge_label(['a','b','c','d'], max_length=1), 'a,…,d')

    def test_str_raises_type_error(self):
        with self.assertRaises(TypeError):
            get_edge_label('a')


class TestGetEdgeLabelPDA(unittest.TestCase):

    pass


class TestGetEdgeLabelTM(unittest.TestCase):

    pass