import unittest
from autolang.backend.regex.gnfa import GNFA
from autolang import NFA

class TestGNFA(unittest.TestCase):

    def test_init(self):
        gnfa = GNFA('a.b*+c')
        self.assertEqual(gnfa.states, ['s0', 't'])
        self.assertEqual(set(gnfa.alphabet), set(('a', 'b', 'c')))
        self.assertEqual(gnfa.edges, [('s0', 't', 'a.b*+c')])
        self.assertEqual(gnfa.start, 's0')
        self.assertEqual(gnfa.accept, 't')

    def test_new_state(self):
        gnfa = GNFA('a')
        gnfa.states.append(gnfa.new_state())
        self.assertEqual(gnfa.states, ['s0', 't', 's1'])
        gnfa.states.append(gnfa.new_state())
        self.assertEqual(gnfa.states, ['s0', 't', 's1', 's2'])
        gnfa.states.append(gnfa.new_state())
        self.assertEqual(gnfa.states, ['s0', 't', 's1', 's2', 's3'])

    def test_eliminate_union(self):
        gnfa = GNFA('a+b')
        gnfa.eliminate_union('s0', 't', 'a', 'b', 'a+b')
        self.assertEqual(set(gnfa.edges), {('s0', 't', 'a'), ('s0', 't', 'b')})
        # Test enclosing bracket
        gnfa = GNFA('(a+b)')
        gnfa.eliminate_union('s0', 't', 'a', 'b', '(a+b)')
        self.assertEqual(set(gnfa.edges), {('s0', 't', 'a'), ('s0', 't', 'b')})

    def test_eliminate_concat(self):
        gnfa = GNFA('a.b')
        gnfa.eliminate_concat('s0', 't', 'a', 'b', 'a.b')
        self.assertEqual(set(gnfa.states), {'s0', 's1', 't'})
        self.assertEqual(set(gnfa.edges), {('s0', 's1', 'a'), ('s1', 't', 'b')})
        # Test enclosing bracket
        gnfa = GNFA('(a.b)')
        gnfa.eliminate_concat('s0', 't', 'a', 'b', '(a.b)')
        self.assertEqual(set(gnfa.states), {'s0', 's1', 't'})
        self.assertEqual(set(gnfa.edges), {('s0', 's1', 'a'), ('s1', 't', 'b')})

    def test_eliminate_star(self):
        gnfa = GNFA('a*')
        gnfa.eliminate_star('s0', 't', 'a', 'a*')
        self.assertEqual(set(gnfa.states), {'s0', 's1', 't'})
        self.assertEqual(set(gnfa.edges), {('s0', 's1', ''), ('s1', 't', ''), ('s1', 's1', 'a')})
        # Test enclosing bracket
        gnfa = GNFA('(a*)')
        gnfa.eliminate_star('s0', 't', 'a', '(a*)')
        self.assertEqual(set(gnfa.states), {'s0', 's1', 't'})
        self.assertEqual(set(gnfa.edges), {('s0', 's1', ''), ('s1', 't', ''), ('s1', 's1', 'a')})

    def test_eliminate(self):
        pass # This should be covered by the above tests, TODO write later

    def test_to_nfa(self):
        gnfa = GNFA('a') # Deliberately choose GNFA that is already valid NFA
        nfa = gnfa.to_nfa()
        self.assertIsInstance(nfa, NFA)
        self.assertEqual(nfa.transition.function, {('s0', 'a'): ('t',)})
        self.assertEqual(set(nfa.states), {'s0', 't'})
        self.assertEqual(set(nfa.alphabet), {'a'})
        self.assertEqual(nfa.start, 's0')
        self.assertEqual(nfa.accept, {'t'})


if __name__ == '__main__':
    unittest.main()