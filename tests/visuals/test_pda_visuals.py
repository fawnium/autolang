import unittest
from autolang.visuals.pda_visuals import (config_to_str,
                                          next_configs_to_str,
                                          _transition_table_pda,
                                          _get_pda_digraph)
from setup_automata import pda1

class TestConfigToStr(unittest.TestCase):

    pass


class TestNextConfigsToStr(unittest.TestCase):

    pass


class TestTransitionTablePDA(unittest.TestCase):
    '''
    NOTE these tests are brittle and will fail if table formatting changes in any way.
    Not sure of a better way to test.
    '''
    def test_pda_1(self):
        intended = '''╔══════╦════════════╦════════════╦═══════════════════╗
║Input:║0           ║1           ║ε                  ║
╠══════╬═╦═╦════════╬═╦════════╦═╬════════╦═╦════════╣
║Stack:║$║0║ε       ║$║0       ║ε║$       ║0║ε       ║
╠══════╬═╬═╬════════╬═╬════════╬═╬════════╬═╬════════╣
║q1    ║ ║ ║        ║ ║        ║ ║        ║ ║{(q2,$)}║
╠══════╬═╬═╬════════╬═╬════════╬═╬════════╬═╬════════╣
║q2    ║ ║ ║{(q2,0)}║ ║{(q3,ε)}║ ║        ║ ║        ║
╠══════╬═╬═╬════════╬═╬════════╬═╬════════╬═╬════════╣
║q3    ║ ║ ║        ║ ║{(q3,ε)}║ ║{(q4,ε)}║ ║        ║
╠══════╬═╬═╬════════╬═╬════════╬═╬════════╬═╬════════╣
║q4    ║ ║ ║        ║ ║        ║ ║        ║ ║        ║
╚══════╩═╩═╩════════╩═╩════════╩═╩════════╩═╩════════╝
'''
        actual = pda1.transition_table(output=False)
        self.assertEqual(intended, actual)


class TestGetPDADigraph(unittest.TestCase):

    pass