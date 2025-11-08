import unittest
from autolang.visuals.utils_visuals import (eps,
                                            get_edge_label,
                                            get_edge_label_pda,
                                            get_edge_label_tm)
from autolang.visuals.magic_chars import RIGHT_ARROW, ELLIPSIS, EPSILON

class TestEps(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(eps(''), EPSILON)

    def test_nonempty(self):
        self.assertEqual(eps('a'), 'a')


class TestGetEdgeLabel(unittest.TestCase):

    def test_single_letter(self):
        self.assertEqual(get_edge_label(['a']), 'a')
        self.assertEqual(get_edge_label(['']),  EPSILON)

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

    def test_single_item(self):
        self.assertEqual(get_edge_label_pda([('a','b','c')]), 'a,b' + RIGHT_ARROW + 'c')
        self.assertEqual(get_edge_label_pda([('','b','c')]),  EPSILON + ',b' + RIGHT_ARROW + 'c')
        self.assertEqual(get_edge_label_pda([('a','','c')]),  'a,' + EPSILON + RIGHT_ARROW + 'c')
        self.assertEqual(get_edge_label_pda([('a','b','')]),  'a,b' + RIGHT_ARROW + EPSILON)

    def test_multiple_items(self):
        items = [('a','a','a'), ('a','b','c')]
        self.assertEqual(get_edge_label_pda(items), 'a,a' + RIGHT_ARROW + 'a\na,b' + RIGHT_ARROW + 'c')

    def test_abbreviate(self):
        items = [('a','a','a'), ('a','b','b'), ('a','c','c'),('a','d','d')]
        self.assertEqual(get_edge_label_pda(items), 'a,a' + RIGHT_ARROW + 'a\n' + ELLIPSIS + '\na,d' + RIGHT_ARROW + 'd')

    def test_invalid_raises_type_error(self):
        with self.assertRaises(TypeError):
            get_edge_label_pda(('a','a','a')) # Tuple not nested
        with self.assertRaises(TypeError):
            get_edge_label_pda([('a','a')]) # Tuple wrong length
        with self.assertRaises(TypeError):
            get_edge_label_pda([(1,'a','a')]) # Symbol is int, should be str

class TestGetEdgeLabelTM(unittest.TestCase):

    def test_single_item(self):
        self.assertEqual(get_edge_label_tm([('a','b','R')]), 'a' + RIGHT_ARROW + 'b,R')
        self.assertEqual(get_edge_label_tm([('a','a','R')]), 'a' + RIGHT_ARROW + 'R') # Letter not changed

    def test_multiple_items(self):
        items = [('a','x','R'), ('b','x','R')]
        self.assertEqual(get_edge_label_tm(items), 'a' + RIGHT_ARROW + 'x,R\nb' + RIGHT_ARROW + 'x,R')

    def test_abbreviate(self):
        items = [('a','x','R'), ('b','x','R'), ('c','x','R'), ('d','x','R')]
        self.assertEqual(get_edge_label_tm(items), 'a' + RIGHT_ARROW + 'x,R\n' + ELLIPSIS + '\nd' + RIGHT_ARROW + 'x,R')
    
    def test_invalid_raises_type_error(self):
        with self.assertRaises(TypeError):
            get_edge_label_pda(('a','b','R')) # Tuple not nested
        with self.assertRaises(TypeError):
            get_edge_label_pda([('a','R')]) # Tuple wrong length
        with self.assertRaises(TypeError):
            get_edge_label_pda([(1,'b','R')]) # Symbol is int, should be str