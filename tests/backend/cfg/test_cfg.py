import unittest

from autolang.backend.cfg.cfg import CFG

class TestInit(unittest.TestCase):

    def test_invalid_start(self):
        rules = {'A': ['a'], 'B': ['b']}
        with self.assertRaises(ValueError):
            CFG(rules, 'C')

    # rules init handled by _canonise_rules()
    # nonterminals and terminals init handled by _extract()


class TestCanoniseRules(unittest.TestCase):

    # Trivial CFG allowed currently
    def test_empty(self):
        rules = {}
        self.assertEqual(CFG._canonise_rules(rules), {})

    def test_erule(self):
        # Unwrapped
        rules = {'A': ['']}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('',),)})

        # Wrapped
        rules = {'A': [['']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('',),)})

    def test_single_unit_rule(self):
        # Unwrapped symbol
        rules = {'A': ['a']}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('a',),)})
        
        # Wrapped symbol
        rules1 = {'A': [['a']]}
        self.assertEqual(CFG._canonise_rules(rules1), {'A': (('a',),)})

    def test_single_compound_rule(self):
        rules = {'A': [['a', 'b']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('a', 'b'),)})

    def test_multiple_rules_mixed(self):
        # Unit unwrapped, compound, unit wrapped
        rules = {'A': ['a', ['b', 'c'], ['d']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('a',), ('d',), ('b', 'c'))})

    def test_nonduplication(self):
        # Unit rule
        rules = {'A': ['a', 'a', ['a']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('a',),)})

        # Compound rule
        rules1 = {'A': [['a', 'b'], ['a', 'b']]}
        self.assertEqual(CFG._canonise_rules(rules1), {'A': (('a', 'b'),)})

        # Should NOT deduplicate as order is important
        rules2 = {'A': [['a', 'b'], ['b', 'a']]}
        self.assertEqual(CFG._canonise_rules(rules2), {'A': (('a', 'b'), ('b', 'a'))})

    def test_sorting(self):
        # Use set for nondeterministic ordering
        rules = {'A': {('a',), ('b', 'a'), ('a', 'b'), ('b',)}}
        # Expect lenlex order
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('a',), ('b',), ('a', 'b'), ('b', 'a'))})

    def test_string_not_split(self):
        # 'abc' is single symbol, not ('a','b','c')
        rules = {'A': ['abc']}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('abc',),)})

        # Wrapped
        rules1 = {'A': [['abc']]}
        self.assertEqual(CFG._canonise_rules(rules1), {'A': (('abc',),)})

    def test_multiple_nonterminals(self):
        rules = {'A': ['a', ['b', 'c']],
                 'B': ['d', ['e', 'f']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('a',), ('b', 'c')), 'B': (('d',), ('e', 'f'))})



    # Invalid input

    def test_not_dict(self):
        rules = ['A']
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    def test_nonstring_nonterminal(self):
        rules = {1: ['a']}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    def test_substitutions_not_iterable(self):
        rules = {'A': 1}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    # TODO ordered NOT just iterable!
    def test_sub_not_iterable(self):
        rules = {'A': [1, ['a','b']]} # First sub fails, 2nd correct
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    def test_nonstring_symbol(self):
        rules = {'A': [[1, 'a']]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    def test_nesting_too_deep(self):
        rules = {'A': [[['a']]]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)





if __name__ == '__main__':
    unittest.main()