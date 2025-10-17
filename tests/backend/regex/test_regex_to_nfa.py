import unittest
from autolang import regex_to_nfa, NFA
from autolang.backend.utils import words_to_length_from_regex

class TestRegexToNFA(unittest.TestCase):

    def test_empty(self):
        nfa = regex_to_nfa('')
        self.assertEqual(set(nfa.L(4)), {''})

    def test_a(self):
        nfa = regex_to_nfa('a')
        self.assertEqual(set(nfa.L(4)), {'a'})

    def test_a_plus_b(self):
        nfa = regex_to_nfa('a+b')
        self.assertEqual(set(nfa.L(4)), {'a', 'b'})

    def test_ab(self):
        nfa = regex_to_nfa('ab')
        self.assertEqual(set(nfa.L(4)), {'ab'})

    def test_a_star(self):
        nfa = regex_to_nfa('a*')
        self.assertEqual(set(nfa.L(4)), {'', 'a', 'aa', 'aaa', 'aaaa'})

    def test_a_star_b_star(self):
        nfa = regex_to_nfa('a*b*')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b'], 'a*b*')))

    def test_a_plus_b_star(self):
        nfa = regex_to_nfa('(a+b)*')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b'], '(a+b)*')))

    def test_a_b_plus_c(self):
        nfa = regex_to_nfa('a(b+c)')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b', 'c'], 'a(b+c)')))

    def test_ab_star(self):
        nfa = regex_to_nfa('(ab)*')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b'], '(ab)*')))

    def test_a_plus_b_star_c(self):
        nfa = regex_to_nfa('a+(b*c)')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b', 'c'], 'a+(b*c)')))

    def test_a_star_plus_b_star_star(self):
        nfa = regex_to_nfa('((a*)+(b*))*')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b'], '((a*)+(b*))*')))

    def test_a_b_plus_c_star_d(self):
        nfa = regex_to_nfa('(a(b+c)*)d')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b', 'c', 'd'], '(a(b+c)*)d')))

    def test_a_plus_b_star_c(self):
        nfa = regex_to_nfa('a+b*c')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b', 'c'], 'a+b*c')))

    def test_a_star_b_plus_c_star(self):
        nfa = regex_to_nfa('a*(b+c)*')
        self.assertEqual(set(nfa.L(4)), set(words_to_length_from_regex(4, ['a', 'b', 'c'], 'a*(b+c)*')))

    def test_invalid_input(self):
        pass


if __name__ == '__main__':
    unittest.main()