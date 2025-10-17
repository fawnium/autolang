import unittest
from autolang import PDA

class TestPDA(unittest.TestCase):

    def setUp(self):
        # Example 1 in examples/pda_examples.py
        self.tran = {
            ('q1', '', ''): (('q2', '$'),),
            ('q2', '0', ''): (('q2', '0'),),
            ('q2', '1', '0'): (('q3', ''),),
            ('q3', '1', '0'): (('q3', ''),),
            ('q3', '', '$'): (('q4', ''),)
        }
        self.start = 'q1'
        self.accept = ['q1', 'q4']

    def test_init(self):
        pda = PDA(self.tran, self.start, self.accept)
        self.assertEqual(pda.transition.function, self.tran)
        self.assertEqual(set(pda.states), {'q1', 'q2', 'q3', 'q4'})
        self.assertEqual(set(pda.input_alphabet), {'0', '1'})
        self.assertEqual(set(pda.stack_alphabet), {'$', '0'})
        self.assertEqual(pda.start, self.start)
        self.assertEqual(set(pda.accept), set(self.accept))

    def test_accepts(self):
        pda = PDA(self.tran, self.start, self.accept)
        self.assertTrue(pda.accepts(''))
        self.assertTrue(pda.accepts('01'))
        self.assertTrue(pda.accepts('0011'))
        self.assertTrue(pda.accepts('000111'))
        self.assertTrue(pda.accepts('00001111'))

        self.assertFalse(pda.accepts('001'))
        self.assertFalse(pda.accepts('011'))
        self.assertFalse(pda.accepts('10'))

    def test_L(self):
        pda = PDA(self.tran, self.start, self.accept)
        language_10 = {'', '01', '0011', '000111', '00001111', '0000011111'}
        self.assertEqual(set(pda.L(10)), language_10)

    def test_invalid_start(self):
        with self.assertRaises(ValueError):
            pda = PDA(self.tran, 'qx', self.accept)

    def test_invalid_accept(self):
        with self.assertRaises(ValueError):
            pda = PDA(self.tran, self.start, ['q1', 'qx'])

    def test_next_configs(self):
        pass # TODO later


if __name__ == '__main__':
    unittest.main()