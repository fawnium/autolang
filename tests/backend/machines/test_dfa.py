import unittest
from autolang import DFA
from autolang.backend.utils import words_to_length_from_regex

class TestDFA(unittest.TestCase):

    def setUp(self):
        # Example 1 in examples/dfa_examples.py
        self.tran = {
            ('q1', '0'): 'q1',
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q3',
            ('q2', '1'): 'q2',
            ('q3', '0'): 'q2',
            ('q3', '1'): 'q2'
        }
        self.start = 'q1'
        self.accept = ['q2']

    def test_init(self):
        dfa = DFA(self.tran, self.start, self.accept)
        self.assertEqual(dfa.transition.function, self.tran)
        self.assertEqual(set(dfa.states), {'q1', 'q2', 'q3'})
        self.assertEqual(set(dfa.alphabet), {'0', '1'})
        self.assertEqual(dfa.start, self.start)
        self.assertEqual(set(dfa.accept), set(self.accept))

    def test_accepts(self):
        dfa = DFA(self.tran, self.start, self.accept)
        self.assertTrue(dfa.accepts('1'))
        self.assertTrue(dfa.accepts('100'))
        self.assertTrue(dfa.accepts('10000'))
        self.assertTrue(dfa.accepts('01'))
        self.assertTrue(dfa.accepts('0100'))
        self.assertTrue(dfa.accepts('010000'))

        self.assertFalse(dfa.accepts(''))
        self.assertFalse(dfa.accepts('0'))
        self.assertFalse(dfa.accepts('00'))
        self.assertFalse(dfa.accepts('010'))
        self.assertFalse(dfa.accepts('01000'))
        self.assertFalse(dfa.accepts('10'))
        self.assertFalse(dfa.accepts('1000'))

    def test_L(self):
        dfa = DFA(self.tran, self.start, self.accept)
        self.assertEqual(set(dfa.L(10)), set(words_to_length_from_regex(10, ['0', '1'], '(0+1)*1(00)*')))

    def test_invalid_start(self):
        with self.assertRaises(ValueError):
            dfa = DFA(self.tran, 'qx', self.accept)

    def test_invalid_accept(self):
        with self.assertRaises(ValueError):
            dfa = DFA(self.tran, self.start, ['qx'])
        with self.assertRaises(ValueError):
            dfa = DFA(self.tran, self.start, 'qx') # Not wrapped in container


if __name__ == '__main__':
    unittest.main()