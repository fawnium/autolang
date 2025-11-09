import unittest
import networkx as nx

from autolang.visuals.pda_visuals import (config_to_str,
                                          next_configs_to_str,
                                          _transition_table_pda,
                                          _get_pda_digraph)
from autolang.visuals.magic_chars import EPSILON, RIGHT_ARROW
from autolang.visuals.settings_visuals import DEFAULT_ACCEPT_COL, DEFAULT_REJECT_COL
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

    def test_pda_1(self):
        digraph = _get_pda_digraph(pda1.transition, pda1.start, pda1.accept, filename='test')

        # States and edges
        self.assertEqual(set(digraph.nodes), set(pda1.states))
        self.assertEqual(set(digraph.edges), {('q1','q2'), ('q2','q2'), ('q2','q3'), ('q3','q3'), ('q3','q4')})

        # Node colors
        self.assertEqual(digraph.nodes['q1']['color'], DEFAULT_ACCEPT_COL)
        self.assertEqual(digraph.nodes['q2']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q3']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q4']['color'], DEFAULT_ACCEPT_COL)

        # Edge labels
        edge_labels = nx.get_edge_attributes(digraph, 'label')
        self.assertEqual(edge_labels[('q1','q2')], EPSILON + ',' + EPSILON + RIGHT_ARROW + '$')
        self.assertEqual(edge_labels[('q2','q2')], '0,' + EPSILON + RIGHT_ARROW + '0')
        self.assertEqual(edge_labels[('q2','q3')], '1,0' + RIGHT_ARROW + EPSILON)
        self.assertEqual(edge_labels[('q3','q3')], '1,0' + RIGHT_ARROW + EPSILON)
        self.assertEqual(edge_labels[('q3','q4')], EPSILON + ',$' + RIGHT_ARROW + EPSILON)

        # Metadata
        self.assertEqual(digraph.graph['start'], 'q1')
        self.assertEqual(set(digraph.graph['accept']), set(('q1','q4')))
        self.assertEqual(digraph.graph['title'], 'PDA with 4 states, input alphabet {0,1}, stack {$,0}')
        self.assertEqual(digraph.graph['kind'], 'PDA')
        self.assertEqual(digraph.graph['filename'], 'test')