import unittest
from autolang.visuals.nfa_visuals import (next_states_to_str,
                                          _transition_table_nfa,
                                          _get_nfa_digraph)
from autolang.visuals.magic_chars import EMPTY
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

    pass