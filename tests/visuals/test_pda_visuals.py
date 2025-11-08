import unittest
from autolang.visuals.pda_visuals import (config_to_str,
                                          next_configs_to_str,
                                          _transition_table_pda,
                                          _get_pda_digraph)
from autolang.visuals.magic_chars import EPSILON
from setup_automata import pda1

class TestConfigToStr(unittest.TestCase):

    def test_epsilon(self):
        self.assertEqual(config_to_str(('q0','')), '(q0,' + EPSILON + ')')

    def test_letter(self):
        self.assertEqual(config_to_str(('q0','a')), '(q0,a)')


class TestNextConfigsToStr(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(next_configs_to_str(tuple()), ' ')

    def test_single_config(self):
        self.assertEqual(next_configs_to_str((('q0','a'),)), '{(q0,a)}')

    def test_multiple_configs(self):
        configs = (('q0','a'), ('q1','b'))
        self.assertEqual(next_configs_to_str(configs), '{(q0,a),(q1,b)}')

    def test_sorted(self):
        configs = (('q1','b'), ('q1','a'), ('q11', 'a'), ('q0','b'), ('q0','a'))
        self.assertEqual(next_configs_to_str(configs), '{(q0,a),(q0,b),(q1,a),(q1,b),(q11,a)}')

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