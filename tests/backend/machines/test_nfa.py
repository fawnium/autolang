import unittest
from autolang import NFA
from autolang.backend.utils import words_to_length_from_regex

class TestNFA(unittest.TestCase):

    def setUp(self):
        # Example 1 in examples/nfa_examples.py
        self.tran = {
            ('q1', '0'): ('q1',), 
            ('q1', '1'): ('q1', 'q2'), 
            ('q2', ''): ('q3',),
            ('q2', '0'): ('q3',),
            ('q3', '1'): ('q4',),
            ('q4', '0'): ('q4',),
            ('q4', '1'): ('q4',) 
        }
        self.start = 'q1'
        self.accept = ['q4']

    def test_init(self):
        nfa = NFA(self.tran, self.start, self.accept)
        self.assertEqual(nfa.transition.function, self.tran)
        self.assertEqual(set(nfa.states), {'q1', 'q2', 'q3', 'q4'})
        self.assertEqual(set(nfa.alphabet), {'0', '1'})
        self.assertEqual(nfa.start, self.start)
        self.assertEqual(set(nfa.accept), set(self.accept))

    def test_accepts(self):
        nfa = NFA(self.tran, self.start, self.accept)
        self.assertTrue(nfa.accepts('11'))
        self.assertTrue(nfa.accepts('011'))
        self.assertTrue(nfa.accepts('110'))
        self.assertTrue(nfa.accepts('111'))
        self.assertTrue(nfa.accepts('0110'))
        self.assertTrue(nfa.accepts('101'))
        self.assertTrue(nfa.accepts('0101'))
        self.assertTrue(nfa.accepts('1010'))
        self.assertTrue(nfa.accepts('1101'))
        self.assertTrue(nfa.accepts('1011'))

        self.assertFalse(nfa.accepts(''))
        self.assertFalse(nfa.accepts('0'))
        self.assertFalse(nfa.accepts('00'))
        self.assertFalse(nfa.accepts('1'))
        self.assertFalse(nfa.accepts('01'))
        self.assertFalse(nfa.accepts('10'))

    def test_L(self):
        nfa = NFA(self.tran, self.start, self.accept)
        self.assertEqual(set(nfa.L(10)), set(words_to_length_from_regex(10, ['0', '1'], '(0+1)*((11)+(101))(0+1)*')))

    def test_invalid_start(self):
        with self.assertRaises(ValueError):
            nfa = NFA(self.tran, 'qx', self.accept)

    def test_invalid_accept(self):
        with self.assertRaises(ValueError):
            nfa = NFA(self.tran, self.start, ['qx'])
        with self.assertRaises(ValueError):
            nfa = NFA(self.tran, self.start, 'qx') # Not wrapped in container

    def test_next_states(self):
        pass

    def test_transition_table(self):
        pass

    def test_transition_diagram(self):
        pass



if __name__ == '__main__':
    unittest.main()