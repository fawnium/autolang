import unittest
from autolang import TM

class TestTM(unittest.TestCase):

    def setUp(self):
        # Example 1 in examples/tm_examples.py
        self.tran = {
            ('q1', '#'): ('q8', '#', 'R'),
            ('q1', '0'): ('q2', 'x', 'R'),
            ('q1', '1'): ('q3', 'x', 'R'),
            ('q1', '_'): ('qr', '_', 'R'),
            ('q1', 'x'): ('qr', 'x', 'R'),
            ('q2', '#'): ('q4', '#', 'R'),
            ('q2', '0'): ('q2', '0', 'R'),
            ('q2', '1'): ('q2', '1', 'R'),
            ('q3', '#'): ('q5', '#', 'R'),
            ('q3', '0'): ('q3', '0', 'R'),
            ('q3', '1'): ('q3', '1', 'R'),
            ('q4', '0'): ('q6', 'x', 'L'),
            ('q4', 'x'): ('q4', 'x', 'R'),
            ('q5', '1'): ('q6', 'x', 'L'),
            ('q5', 'x'): ('q5', 'x', 'R'),
            ('q6', '#'): ('q7', '#', 'L'),
            ('q6', '0'): ('q6', '0', 'L'),
            ('q6', '1'): ('q6', '1', 'L'),
            ('q6', 'x'): ('q6', 'x', 'L'),
            ('q7', '0'): ('q7', '0', 'L'),
            ('q7', '1'): ('q7', '1', 'L'),
            ('q7', 'x'): ('q1', 'x', 'R'),
            ('q8', '_'): ('qa', '_', 'R'),
            ('q8', 'x'): ('q8', 'x', 'R'),
        }
        self.start = 'q1'
        self.accept = 'qa'
        self.reject = 'qr'
        self.reserved_letters = ['x']

    def test_init(self):
        tm = TM(self.tran, self.start, self.accept, self.reject, self.reserved_letters)
        self.assertEqual(tm.transition.function, self.tran)
        self.assertEqual(set(tm.states), {'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'qa', 'qr'})
        self.assertEqual(set(tm.input_alphabet), {'#', '0', '1'})
        self.assertEqual(set(tm.tape_alphabet), {'#', '0', '1', '_', 'x'})
        self.assertEqual(tm.start, self.start)
        self.assertEqual(tm.accept, self.accept)
        self.assertEqual(tm.reject, self.reject)

    def test_accepts(self):
        tm = TM(self.tran, self.start, self.accept, self.reject, self.reserved_letters)
        self.assertTrue(tm.accepts('#'))
        self.assertTrue(tm.accepts('0#0'))
        self.assertTrue(tm.accepts('1#1'))
        self.assertTrue(tm.accepts('00#00'))
        self.assertTrue(tm.accepts('01#01'))
        self.assertTrue(tm.accepts('10#10'))
        self.assertTrue(tm.accepts('11#11'))
        self.assertTrue(tm.accepts('101#101'))

        self.assertFalse(tm.accepts(''))
        self.assertFalse(tm.accepts('0#'))
        self.assertFalse(tm.accepts('1#'))
        self.assertFalse(tm.accepts('0#1'))
        self.assertFalse(tm.accepts('10#01'))

    def test_compute(self):
        tm = TM(self.tran, self.start, self.accept, self.reject, self.reserved_letters)
        self.assertEqual(tm.compute('#')[1],       ('#', '_', '_'))
        self.assertEqual(tm.compute('0#0')[1],     ('x', '#', 'x', '_', '_'))
        self.assertEqual(tm.compute('1#1')[1],     ('x', '#', 'x', '_', '_'))
        self.assertEqual(tm.compute('00#00')[1],   ('x', 'x', '#', 'x', 'x', '_', '_'))
        self.assertEqual(tm.compute('01#01')[1],   ('x', 'x', '#', 'x', 'x', '_', '_'))
        self.assertEqual(tm.compute('10#10')[1],   ('x', 'x', '#', 'x', 'x', '_', '_'))
        self.assertEqual(tm.compute('11#11')[1],   ('x', 'x', '#', 'x', 'x', '_', '_'))
        self.assertEqual(tm.compute('101#101')[1], ('x', 'x', 'x', '#', 'x', 'x', 'x', '_', '_'))

        self.assertEqual(tm.compute('')[1],        ('_', '_'))
        self.assertEqual(tm.compute('0#')[1],      ('x', '#', '_', '_'))
        self.assertEqual(tm.compute('1#')[1],      ('x', '#', '_', '_'))
        self.assertEqual(tm.compute('0#1')[1],     ('x', '#', '1', '_'))
        self.assertEqual(tm.compute('10#01')[1],   ('x', '0', '#', '0', '1'))

    def test_L(self):
        tm = TM(self.tran, self.start, self.accept, self.reject, self.reserved_letters)
        language_8 = {'#', '0#0', '1#1', '00#00', '01#01', '10#10', '11#11', '000#000', 
                      '001#001', '010#010', '011#011', '100#100', '101#101', '110#110', 
                      '111#111'}
        self.assertEqual(set(tm.L(8)), language_8)

    def test_invalid_start(self):
        with self.assertRaises(ValueError):
            tm = TM(self.tran, 'qx', self.accept, self.reject, self.reserved_letters)

    def test_move(self):
        pass # TODO later

    def test_next_config(self):
        pass # TODO later

    def test_transition_table(self):
        pass

    def test_transition_diagram(self):
        pass

    def test_run(self):
        pass # Redundant as covered by testing accepts() and compute()


if __name__ == '__main__':
    unittest.main()
    