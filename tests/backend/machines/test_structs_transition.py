import unittest
from autolang.backend.machines.structs_transition import TransitionDFA, TransitionNFA, TransitionPDA, TransitionTM

class TestTransitionDFA(unittest.TestCase):

    def setUp(self):
        # Valid DFA transition func to use later
        self.valid_func = {
            ('q1', '0'): 'q1',
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q3',
            ('q2', '1'): 'q2',
            ('q3', '0'): 'q2',
            ('q3', '1'): 'q2'
        }

    def test_valid_func(self):
        tran = TransitionDFA(self.valid_func) # Shouldn't raise error
        self.assertTrue(tran.validate_type())
        self.assertTrue(tran.validate_fullness())
        self.assertEqual(set(tran.states), {'q1', 'q2', 'q3'})
        self.assertEqual(set(tran.alphabet), {'0', '1'})

    def test_incomplete_func(self):
        # Missing key `('q1', '1')`
        func = {
            ('q1', '0'): 'q1',

            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        with self.assertRaises(ValueError):
            tran = TransitionDFA(func)

    def test_invalid_func_type(self):
        # Func is a list not a dict
        func = [
            ('q1', '0', 'q1'),
            ('q1', '1', 'q2'),
            ('q2', '0', 'q1'),
            ('q2', '1', 'q2')
        ]
        with self.assertRaises(TypeError):
            tran = TransitionDFA(func)

    def test_invalid_key_type(self):
        func1 = {
            'q10' : 'q1', # Key is str not tuple
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        func2 = {
            ('q1',): 'q1', # Key is too short
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        func3 = {
            ('q1', '0', 'X'): 'q1', # Key is too long
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        func4 = {
            (1, '0'): 'q1', # State is wrong type
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        func5 = {
            ('q1', 0): 'q1', # Letter is wrong type
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        with self.assertRaises(TypeError):
            tran1 = TransitionDFA(func1)
        with self.assertRaises(TypeError):
            tran2 = TransitionDFA(func2)
        with self.assertRaises(TypeError):
            tran3 = TransitionDFA(func3)
        with self.assertRaises(TypeError):
            tran4 = TransitionDFA(func4)
        with self.assertRaises(TypeError):
            tran5 = TransitionDFA(func5)

    def test_invalid_value_type(self):
        func1 = {
            ('q1', '0'): 1, # Value is int not str
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        func2 = {
            ('q1', '0'): ('q1',), # Value is tuple not str
            ('q1', '1'): 'q2',
            ('q2', '0'): 'q1',
            ('q2', '1'): 'q2'
        }
        with self.assertRaises(TypeError):
            tran1 = TransitionDFA(func1)
        with self.assertRaises(TypeError):
            tran2 = TransitionDFA(func2)

    def test_dunder_get(self):
        tran = TransitionDFA(self.valid_func)
        self.assertEqual(tran[('q1', '0')], 'q1')
        with self.assertRaises(KeyError):
            tran[('qx', 'x')]

    def test_get(self):
        tran = TransitionDFA(self.valid_func)
        self.assertEqual(tran.get(('q1', '0')), 'q1')
        self.assertEqual(tran.get(('qx', 'x')), None)

    def test_dunder_contains(self):
        tran = TransitionDFA(self.valid_func)
        self.assertIn(('q1', '0'), tran) # Valid key
        self.assertNotIn(('qx', '0'), tran) # Invalid state
        self.assertNotIn(('q1', 'x'), tran) # Invalid letter

    def test_items(self):
        tran = TransitionDFA(self.valid_func)
        self.assertIn((('q1', '0'), 'q1'), tran.items())

    def test_values(self):
        tran = TransitionDFA(self.valid_func)
        self.assertIn('q1', tran.values())


class TestTransitionNFA(unittest.TestCase):

    def setUp(self):
        self.valid_func = {
        ('q1', '0'): ('q1',), 
        ('q1', '1'): ('q1', 'q2'), 
        ('q2', ''): ('q3',),
        ('q2', '0'): ('q3',),
        ('q3', '1'): ('q4',),
        ('q4', '0'): ('q4',),
        ('q4', '1'): ('q4',) 
        }

    def test_valid_func(self):
        tran = TransitionNFA(self.valid_func) # Shouldn't raise error
        self.assertTrue(tran.validate_type())
        self.assertEqual(set(tran.states), {'q1', 'q2', 'q3', 'q4'})
        self.assertEqual(set(tran.alphabet), {'0', '1'})

    def test_invalid_func_type(self):
        # Func is a list not a dict
        func = [('q1', '0', 'q1')]
        with self.assertRaises(TypeError):
            tran = TransitionNFA(func)

    def test_invalid_key_type(self):
        func1 = {'q10': ('q1',)} # Key is str not tuple
        func2 = {('q1',): ('q1',)} # Key is too short
        func3 = {('q1', '0', 'x'): ('q1',)} # Key is too long
        func4 = {(1, '0'): ('q1',)} # State is wrong type
        func5 = {('q1', 0): ('q1',)} # Letter is wrong type
        with self.assertRaises(TypeError):
            tran1 = TransitionNFA(func1)
        with self.assertRaises(TypeError):
            tran2 = TransitionNFA(func2)
        with self.assertRaises(TypeError):
            tran3 = TransitionNFA(func3)
        with self.assertRaises(TypeError):
            tran4 = TransitionNFA(func4)
        with self.assertRaises(TypeError):
            tran5 = TransitionNFA(func5)

    def test_invalid_value_type(self):
        func1 = {('q1', '0'): 'q1'} # Value is str not tuple
        func2 = {('q1', '0'): (1,)} # Next state is int not str
        func3 = {('q1', '0'): ['q1']} # Value is list not tuple
        func4 = {('q1', '0'): {'q1'}} # Value is set not tuple
        with self.assertRaises(TypeError):
            tran1 = TransitionNFA(func1)
        with self.assertRaises(TypeError):
            tran2 = TransitionNFA(func2)
        with self.assertRaises(TypeError):
            tran3 = TransitionNFA(func3)
        with self.assertRaises(TypeError):
            tran4 = TransitionNFA(func4)

    def test_dunder_get(self):
        tran = TransitionNFA(self.valid_func)
        self.assertEqual(tran[('q1', '0')], ('q1',))
        with self.assertRaises(KeyError):
            tran[('qx', 'x')]

    def test_get(self):
        tran = TransitionNFA(self.valid_func)
        self.assertEqual(tran.get(('q1', '0')), ('q1',))
        self.assertEqual(tran.get(('qx', 'x')), tuple())

    def test_dunder_contains(self):
        tran = TransitionNFA(self.valid_func)
        self.assertIn(('q1', '0'), tran)
        self.assertNotIn(('qx', '0'), tran) # Invalid state
        self.assertNotIn(('q1', 'x'), tran) # Invalid letter

    def test_items(self):
        tran = TransitionNFA(self.valid_func)
        self.assertIn((('q1', '0'), ('q1',)), tran.items())

    def test_values(self):
        tran = TransitionNFA(self.valid_func)
        self.assertIn(('q1',), tran.values())


class TestTransitionPDA(unittest.TestCase):
    
    def setUp(self):
        self.valid_func = {
            ('q1', '', ''): (('q2', '$'),),
            ('q2', '0', ''): (('q2', '0'),),
            ('q2', '1', '0'): (('q3', ''),),
            ('q3', '1', '0'): (('q3', ''),),
            ('q3', '', '$'): (('q4', ''),)
        }

    def test_valid_func(self):
        tran = TransitionPDA(self.valid_func) # Shouldn't raise an error
        self.assertTrue(tran.validate_type())
        self.assertEqual(set(tran.states), {'q1', 'q2', 'q3', 'q4'})
        self.assertEqual(set(tran.input_alphabet), {'0', '1'})
        self.assertEqual(set(tran.stack_alphabet), {'$', '0'})

    def test_invalid_func_type(self):
        # Func is a list not a dict
        func = [('q1', '', '', 'q2', '$')]
        with self.assertRaises(TypeError):
            tran = TransitionPDA(func)

    def test_invalid_key_type(self):
        func1 = {'q1': (('q2', '$'),)} # Key is str not tuple
        func2 = {('q1', ''): (('q2', '$'),)} # Key is too short
        func3 = {('q1', '', '', ''): (('q2', '$'),)} # Key is too long
        func4 = {(1, '', ''): (('q2', '$'),)} # State is wrong type
        func5 = {('q1', 0, ''): (('q2', '$'),)} # Letter is wrong type
        func6 = {('q1', '', 0): (('q2', '$'),)} # Stack top is wrong type
        with self.assertRaises(TypeError):
            tran1 = TransitionPDA(func1)
        with self.assertRaises(TypeError):
            tran2 = TransitionPDA(func2)
        with self.assertRaises(TypeError):
            tran3 = TransitionPDA(func3)
        with self.assertRaises(TypeError):
            tran4 = TransitionPDA(func4)
        with self.assertRaises(TypeError):
            tran5 = TransitionPDA(func5)
        with self.assertRaises(TypeError):
            tran6 = TransitionPDA(func6)

    def test_invalid_value_type(self):
        func1 = {('q1', '', ''): 'q2$'} # Value is str not tuple of 2-tuples
        func2 = {('q1', '', ''): ('q2', '$')} # Missing parent tuple
        func3 = {('q1', '', ''): [('q2', '$')]} # List of 2-tuples not tuple of 2-tuples
        func4 = {('q1', '', ''): (['q2', '$'],)} # Tuple of lists not tuple of 2-tuples
        func5 = {('q1', '', ''): (('q2', '$'))} # Missing comma
        func6 = {('q1', '', ''): (('q1',), ('$',))} # Wrong dimensions
        func7 = {('q1', '', ''): ((2, '$'),)} # State is wrong type
        func8 = {('q1', '', ''): (('q2', 0),)} # Stack push is wrong type
        with self.assertRaises(TypeError):
            tran1 = TransitionPDA(func1)
        with self.assertRaises(TypeError):
            tran2 = TransitionPDA(func2)
        with self.assertRaises(TypeError):
            tran3 = TransitionPDA(func3)
        with self.assertRaises(TypeError):
            tran4 = TransitionPDA(func4)
        with self.assertRaises(TypeError):
            tran5 = TransitionPDA(func5)
        with self.assertRaises(TypeError):
            tran6 = TransitionPDA(func6)
        with self.assertRaises(TypeError):
            tran7 = TransitionPDA(func7)
        with self.assertRaises(TypeError):
            tran8 = TransitionPDA(func8)

    def test_dunder_get(self):
        tran = TransitionPDA(self.valid_func)
        self.assertEqual(tran[('q1', '', '')], (('q2', '$'),))
        with self.assertRaises(KeyError):
            tran[('qx', 'x', 'x')]

    def test_get(self):
        tran = TransitionPDA(self.valid_func)
        self.assertEqual(tran.get(('q1', '', '')), (('q2', '$'),))
        self.assertEqual(tran.get(('qx', 'x', 'x')), tuple())

    def test_dunder_contains(self):
        tran = TransitionPDA(self.valid_func)
        self.assertIn(('q1', '', ''), tran)
        self.assertNotIn(('qx', '', ''), tran) # Invalid state
        self.assertNotIn(('q1', 'x', ''), tran) # Invalid letter
        self.assertNotIn(('q1', '', 'x'), tran) # Invalid stack top

    def test_items(self):
        tran = TransitionPDA(self.valid_func)
        self.assertIn((('q1', '', ''), (('q2', '$'),)), tran.items())
    
    def test_values(self):
        tran = TransitionPDA(self.valid_func)
        self.assertIn((('q2', '$'),), tran.values())


class TestTransitionTM(unittest.TestCase):

    def setUp(self):
        self.valid_func = {
            ('q1', '_'): ('qr', '_', 'R'),
            # ('q1', 'x'): ('qr', 'x', 'R'), # Omit to test automatic insertion
            ('q1', '0'): ('q2', '_', 'R'),
            ('q2', '_'): ('qa', '_', 'R'),
            ('q2', 'x'): ('q2', 'x', 'R'),
            ('q2', '0'): ('q3', 'x', 'R'),
            ('q3', '_'): ('q5', '_', 'L'),
            ('q3', 'x'): ('q3', 'x', 'R'),
            ('q3', '0'): ('q4', '0', 'R'),
            ('q4', '_'): ('qr', '_', 'R'),
            ('q4', 'x'): ('q4', 'x', 'R'),
            ('q4', '0'): ('q3', 'x', 'R'),
            ('q5', '_'): ('q2', '_', 'R'),
            ('q5', 'x'): ('q5', 'x', 'L'),
            ('q5', '0'): ('q5', '0', 'L')
        }
        self.start = 'q1'
        self.accept = 'qa'
        self.reject = 'qr'
        self.reserved_letters = {'x'}

    def test_valid_func(self):
        tran = TransitionTM(self.valid_func, self.accept, self.reject, self.reserved_letters)
        self.assertTrue(tran.validate_type())
        self.assertEqual(set(tran.states), {'q1', 'q2', 'q3', 'q4', 'q5', self.accept, self.reject})
        self.assertEqual(set(tran.input_alphabet), {'0'})
        self.assertEqual(set(tran.tape_alphabet), {'0', '_', 'x'})
        self.assertIn((('q1', 'x'), ('qr', 'x', 'R')), tran.function.items()) # Check missing reject transition was added

    def test_invalid_func_type(self):
        # Func is a list not a dict
        func = [('q1', '_', 'qr', '_', 'R')]
        with self.assertRaises(TypeError):
            tran = TransitionTM(func, self.accept, self.reject, self.reserved_letters)

    def test_invalid_key_type(self):
        func1 = {
            ('q1', '_'): ('qa', '_', 'R'), # Include accept transition to prevent prompt at runtime
            'q10': ('qr', '0', 'R') # Key is str not tuple
        }
        func2 = {
            ('q1', '_'): ('qa', '_', 'R'),
            ('q1',): ('qr', '0', 'R') # Tuple is too short
        }
        func3 = {
            ('q1', '_'): ('qa', '_', 'R'),
            ('q1', '0', 'x'): ('qr', '0', 'R') # Tuple is too long
        }
        func4 = {
            ('q1', '_'): ('qa', '_', 'R'),
            (1, '0'): ('qr', '0', 'R') # State is wrong type
        }
        func5 = {
            ('q1', '_'): ('qa', '_', 'R'),
            ('q1', 0): ('qr', '0', 'R') # Letter is wrong type
        }
        with self.assertRaises(TypeError):
            tran1 = TransitionTM(func1, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran2 = TransitionTM(func2, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran3 = TransitionTM(func3, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran4 = TransitionTM(func4, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran5 = TransitionTM(func5, self.accept, self.reject)

    def test_invalid_value_type(self):
        func1 = {
            ('q1', '_'): ('qa', '_', 'R'), # Include accept transition to prevent prompt at runtime
            ('q1', '0'): 'qr0R' # Value is str not tuple
        }
        func2 = {
            ('q1', '_'): ('qa', '_', 'R'),
            ('q1', '0'): (1, '0', 'R') # State is wrong type
        }
        func3 = {
            ('q1', '_'): ('qa', '_', 'R'),
            ('q1', '0'): ('qr', 0, 'R') # Write is wrong type
        }
        func4 = {
            ('q1', '_'): ('qa', '_', 'R'),
            ('q1', '0'): ('qr', '0', 1) # Direction is wrong type
        }
        func5 = {
            ('q1', '_'): ('qa', '_', 'R'),
            ('q1', '0'): ('qr', '0', 'X') # Invalid direction
        }
        with self.assertRaises(TypeError):
            tran1 = TransitionTM(func1, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran2 = TransitionTM(func2, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran3 = TransitionTM(func3, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran4 = TransitionTM(func4, self.accept, self.reject)
        with self.assertRaises(TypeError):
            tran5 = TransitionTM(func5, self.accept, self.reject)
        
    def test_dunder_get(self):
        tran = TransitionTM(self.valid_func, self.accept, self.reject, self.reserved_letters)
        self.assertEqual(tran[('q1', '_')], ('qr', '_', 'R'))
        with self.assertRaises(KeyError):
            tran[('qx', 'x')]

    def test_get(self):
        tran = TransitionTM(self.valid_func, self.accept, self.reject, self.reserved_letters)
        self.assertEqual(tran.get(('q1', '_')), ('qr', '_', 'R'))
        self.assertEqual(tran.get(('qx', 'x')), None)

    def test_items(self):
        tran = TransitionTM(self.valid_func, self.accept, self.reject, self.reserved_letters)
        self.assertIn((('q1', '_'), ('qr', '_', 'R')), tran.items())

    def test_values(self):
        tran = TransitionTM(self.valid_func, self.accept, self.reject, self.reserved_letters)
        self.assertIn(('qr', '_', 'R'), tran.values())


if __name__ == '__main__':
    unittest.main()