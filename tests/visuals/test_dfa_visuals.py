import unittest
from autolang.visuals.dfa_visuals import _transition_table_dfa, _get_dfa_digraph
from setup_automata import dfa1

class TestTransitionTableDFA(unittest.TestCase):
    '''
    NOTE these tests are brittle and will fail if table formatting changes in any way.
    Not sure of a better way to test.
    '''
    def test_dfa_1(self):
        intended = '''╔══╦══╦══╗
║  ║0 ║1 ║
╠══╬══╬══╣
║q1║q1║q2║
╠══╬══╬══╣
║q2║q3║q2║
╠══╬══╬══╣
║q3║q2║q2║
╚══╩══╩══╝
'''
        actual = dfa1.transition_table(output=False)
        self.assertEqual(intended, actual)
    

class TestGetDFADigraph(unittest.TestCase):

    pass