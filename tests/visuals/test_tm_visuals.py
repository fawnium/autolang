import unittest
import networkx as nx

from autolang.visuals.tm_visuals import (next_config_to_str,
                                          _transition_table_tm,
                                          _get_tm_digraph)
from autolang.visuals.magic_chars import RIGHT_ARROW
from autolang.visuals.settings_visuals import DEFAULT_ACCEPT_COL, DEFAULT_REJECT_COL
from setup_automata import tm1, tm2


class TestNextConfigToStr(unittest.TestCase):

    def test_halting_state(self):
        self.assertEqual(next_config_to_str(('qa','x','R'), ('qa','qr')), 'qa')

    def test_normal_state(self):
        self.assertEqual(next_config_to_str(('q0','x','R'), ('qa','qr')), '(q0,x,R)')


class TestTransitionTableTM(unittest.TestCase):
    '''
    NOTE these tests are brittle and will fail if table formatting changes in any way.
    Not sure of a better way to test.
    '''
    def test_tm_1(self):
        intended = '''╔════════╦════════╦════════╦════════╦════════╦════════╗
║        ║#       ║0       ║1       ║_       ║x       ║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q1      ║(q8,#,R)║(q2,x,R)║(q3,x,R)║qr      ║qr      ║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q2      ║(q4,#,R)║(q2,0,R)║(q2,1,R)║qr      ║qr      ║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q3      ║(q5,#,R)║(q3,0,R)║(q3,1,R)║qr      ║qr      ║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q4      ║qr      ║(q6,x,L)║qr      ║qr      ║(q4,x,R)║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q5      ║qr      ║qr      ║(q6,x,L)║qr      ║(q5,x,R)║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q6      ║(q7,#,L)║(q6,0,L)║(q6,1,L)║qr      ║(q6,x,L)║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q7      ║qr      ║(q7,0,L)║(q7,1,L)║qr      ║(q1,x,R)║
╠════════╬════════╬════════╬════════╬════════╬════════╣
║q8      ║qr      ║qr      ║qr      ║qa      ║(q8,0,R)║
╚════════╩════════╩════════╩════════╩════════╩════════╝
'''
        actual = tm1.transition_table(output=False)
        self.assertEqual(intended, actual)

    
class TestGetTMDigraph(unittest.TestCase):

    # Testing 2 not 1 because 1 has so many transitions
    def test_tm_2(self):
        digraph = _get_tm_digraph(tm2.transition, tm2.start, tm2.accept, tm2.reject, filename='test')

        # Nodes and edges
        self.assertEqual(set(digraph.nodes), set(tm2.states))
        tm_edges = {('q1', 'q2'), ('q1', 'qr'),
                    ('q2', 'q2'), ('q2', 'q3'), ('q2', 'qa'),
                    ('q3', 'q3'), ('q3', 'q4'), ('q3', 'q5'),
                    ('q4', 'q3'), ('q4', 'q4'), ('q4', 'qr'),
                    ('q5', 'q2'), ('q5', 'q5')}
        self.assertEqual(set(digraph.edges), tm_edges)

        # Node colours
        self.assertEqual(digraph.nodes['q1']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q2']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q3']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q4']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['q5']['color'], DEFAULT_REJECT_COL)
        self.assertEqual(digraph.nodes['qa']['color'], DEFAULT_ACCEPT_COL)
        self.assertEqual(digraph.nodes['qr']['color'], 'lightcoral')

        # Edge labels
        edge_labels = nx.get_edge_attributes(digraph, 'label')
        self.assertEqual(edge_labels[('q1','q2')], '0' + RIGHT_ARROW + '_,R')
        self.assertEqual(edge_labels[('q1','qr')], '_' + RIGHT_ARROW + 'R\nx' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q2','q2')], 'x' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q2','q3')], '0' + RIGHT_ARROW + 'x,R')
        self.assertEqual(edge_labels[('q2','qa')], '_' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q3','q3')], 'x' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q3','q4')], '0' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q3','q5')], '_' + RIGHT_ARROW + 'L')
        self.assertEqual(edge_labels[('q4','q3')], '0' + RIGHT_ARROW + 'x,R')
        self.assertEqual(edge_labels[('q4','q4')], 'x' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q4','qr')], '_' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q5','q2')], '_' + RIGHT_ARROW + 'R')
        self.assertEqual(edge_labels[('q5','q5')], '0' + RIGHT_ARROW + 'L\nx' + RIGHT_ARROW + 'L')

        # Metadata
        self.assertEqual(digraph.graph['start'], 'q1')
        self.assertEqual(digraph.graph['accept'], tm2.accept)
        self.assertEqual(digraph.graph['reject'], tm2.reject)
        self.assertEqual(digraph.graph['title'], 'TM with 5 states and input alphabet {0}')
        self.assertEqual(digraph.graph['kind'], 'TM')
        self.assertEqual(digraph.graph['filename'], 'test')