import unittest
from autolang.visuals.nfa_visuals import (next_states_to_str,
                                          _transition_table_nfa,
                                          _get_nfa_digraph)
from setup_automata import nfa1

class TestNextStatesToStr(unittest.TestCase):
    
    pass


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