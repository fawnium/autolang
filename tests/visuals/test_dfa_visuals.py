import unittest
import networkx as nx

from autolang.visuals.dfa_visuals import _transition_table_dfa, _get_dfa_digraph
from autolang.visuals.settings_visuals import DEFAULT_ACCEPT_COL, DEFAULT_REJECT_COL
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

    def test_dfa_1(self):
        digraph = _get_dfa_digraph(dfa1.transition, dfa1.start, dfa1.accept, filename='test')

        # States and edges
        self.assertEqual(set(digraph.nodes), set(dfa1.states))
        self.assertEqual(set(digraph.edges), {('q1','q1'), ('q1','q2'), ('q2','q2'), ('q2','q3'), ('q3','q2')})

        # Node colours
        self.assertEqual(digraph.nodes['q1']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q2']['color'], DEFAULT_ACCEPT_COL)
        self.assertEqual(digraph.nodes['q3']['color'], DEFAULT_REJECT_COL)

        # Edge labels
        edge_labels = nx.get_edge_attributes(digraph, 'label')
        self.assertEqual(edge_labels[('q1','q1')], '0')
        self.assertEqual(edge_labels[('q1','q2')], '1')
        self.assertEqual(edge_labels[('q2','q2')], '1')
        self.assertEqual(edge_labels[('q2','q3')], '0')
        self.assertEqual(edge_labels[('q3','q2')], '0,1')

        # Metadata
        self.assertEqual(digraph.graph['start'], 'q1')
        self.assertEqual(digraph.graph['accept'], ('q2',))
        self.assertEqual(digraph.graph['title'], 'DFA with 3 states and alphabet {0,1}')
        self.assertEqual(digraph.graph['kind'], 'DFA')
        self.assertEqual(digraph.graph['filename'], 'test')
