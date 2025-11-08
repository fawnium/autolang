import unittest
from autolang.visuals.tm_visuals import (next_config_to_str,
                                          _transition_table_tm,
                                          _get_tm_digraph)
from setup_automata import tm1


class TestNextConfigToStr(unittest.TestCase):

    pass


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

    pass