import unittest
from autolang import nfa_to_dfa, NFA, DFA
from autolang.backend.regex.nfa_to_dfa import ConstructDFA

class TestConstructDFA(unittest.TestCase):
    '''
    This will be quite tricky to set up as it requires an existing valid NFA, for which we 
    need to precisely understand the theoretical subset construction.
    As well as the theoretical construction, we need to understand the specific autolang encoding of state 
    names.
    Basically, it is hard to isolate the behaviour from the rest of the files in the project I think.
    It will certainly be possible but there is not enough time right now.
    '''

    pass # TODO


class TestNFA_To_DFA(unittest.TestCase):

    # Example 1 in examples/nfa_examples.py
    def test_nfa_1(self):
        tran = {
            ('q1', '0'): ('q1',), 
            ('q1', '1'): ('q1', 'q2'), 
            ('q2', ''): ('q3',),
            ('q2', '0'): ('q3',),
            ('q3', '1'): ('q4',),
            ('q4', '0'): ('q4',),
            ('q4', '1'): ('q4',) 
        }
        nfa = NFA(tran, 'q1', ['q4'])
        dfa = nfa_to_dfa(nfa)
        self.assertEqual(set(nfa.L(10)), set(dfa.L(10)))


if __name__ == '__main__':
    unittest.main()