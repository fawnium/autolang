import unittest
import networkx as nx

from autolang.visuals.nfa_visuals import (next_states_to_str,
                                          _transition_table_nfa,
                                          _get_nfa_digraph)
from autolang.visuals.magic_chars import EMPTY, EPSILON
from autolang.visuals.settings_visuals import DEFAULT_ACCEPT_COL, DEFAULT_REJECT_COL
from setup_automata import nfa1

class TestNextStatesToStr(unittest.TestCase):
    
    def test_empty(self):
        self.assertEqual(next_states_to_str(tuple()), EMPTY)

    def test_single_state(self):
        self.assertEqual(next_states_to_str(('q0',)), '{q0}')

    def test_multiple_states(self):
        self.assertEqual(next_states_to_str(('q0', 'q1')), '{q0,q1}')

    def test_sorted(self):
        self.assertEqual(next_states_to_str(('q1', 'q0')), '{q0,q1}')


class TestTransitionTableNFA(unittest.TestCase):
    '''
    NOTE these tests are brittle and will fail if table formatting changes in any way.
    Not sure of a better way to test.
    '''
    def test_nfa_1(self):
        intended = '''╔═══════╦═══════╦═══════╦═══════╗
║       ║0      ║1      ║ε      ║
╠═══════╬═══════╬═══════╬═══════╣
║q1     ║{q1}   ║{q1,q2}║∅      ║
╠═══════╬═══════╬═══════╬═══════╣
║q2     ║{q3}   ║∅      ║{q3}   ║
╠═══════╬═══════╬═══════╬═══════╣
║q3     ║∅      ║{q4}   ║∅      ║
╠═══════╬═══════╬═══════╬═══════╣
║q4     ║{q4}   ║{q4}   ║∅      ║
╚═══════╩═══════╩═══════╩═══════╝
'''
        actual = nfa1.transition_table(output=False)
        self.assertEqual(intended, actual)


class TestGetNFADigraph(unittest.TestCase):

    def test_nfa_1(self):
        digraph = _get_nfa_digraph(nfa1.transition, nfa1.start, nfa1.accept, filename='test')

        # States and edges
        self.assertEqual(set(digraph.nodes), set(nfa1.states))
        self.assertEqual(set(digraph.edges), {('q1','q1'), ('q1','q2'), ('q2','q3'), ('q3','q4'), ('q4','q4')})

        # Node colours
        self.assertEqual(digraph.nodes['q1']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q2']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q3']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q4']['color'], DEFAULT_ACCEPT_COL)

        # Edge labels
        edge_labels = nx.get_edge_attributes(digraph, 'label')
        self.assertEqual(edge_labels[('q1','q1')], '0,1')
        self.assertEqual(edge_labels[('q1','q2')], '1')
        self.assertEqual(edge_labels[('q2','q3')], EPSILON + ',0')
        self.assertEqual(edge_labels[('q3','q4')], '1')
        self.assertEqual(edge_labels[('q4','q4')], '0,1')

        # Metadata
        self.assertEqual(digraph.graph['start'], 'q1')
        self.assertEqual(digraph.graph['accept'], ('q4',))
        self.assertEqual(digraph.graph['title'], 'NFA with 4 states and alphabet {0,1}')
        self.assertEqual(digraph.graph['kind'], 'NFA')
        self.assertEqual(digraph.graph['filename'], 'test')