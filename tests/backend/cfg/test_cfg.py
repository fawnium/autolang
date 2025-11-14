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
    def test_empty_cfg(self):
        rules = {}
        self.assertEqual(CFG._canonise_rules(rules), {})

    def test_empty_rules(self):
        rules = {'A': []}
        self.assertEqual(CFG._canonise_rules(rules), {'A': tuple()})

    def test_erule(self):
        # Unwrapped
        rules = {'A': ['']}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('',),)})

        # Wrapped
        rules = {'A': [['']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('',),)})

    # Should be converted to conventional epsilon encoding
    def test_empty_sub(self):
        rules = {'A': [[], ['a']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('',), ('a',))})

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

    def test_deduplication(self):
        # Unit rule
        rules = {'A': ['a', 'a', ['a']]}
        self.assertEqual(CFG._canonise_rules(rules), {'A': (('a',),)})

        # Compound rule
        rules1 = {'A': [['a', 'b'], ['a', 'b']]}
        self.assertEqual(CFG._canonise_rules(rules1), {'A': (('a', 'b'),)})

        # e-rule
        rules2 = {'A': ['', [''], [], []]}
        self.assertEqual(CFG._canonise_rules(rules2), {'A': (('',),)})

        # Should NOT deduplicate as order is important
        rules3 = {'A': [['a', 'b'], ['b', 'a']]}
        self.assertEqual(CFG._canonise_rules(rules3), {'A': (('a', 'b'), ('b', 'a'))})

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

    def test_empty_nonterminal(self):
        rules = {'': ['a', ['a', 'b']]}
        with self.assertRaises(ValueError):
            CFG._canonise_rules(rules)

    def test_substitutions_not_iterable(self):
        rules = {'A': 1}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    def test_sub_not_sequence(self):
        # Sub not even container
        rules = {'A': [1]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

        # Sub container but not ordered
        rules1 = {'A': [{'a', 'b'}]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules1)

    def test_epsilon_in_compound_rule(self):
        rules = {'A': [['a', '', 'b']]}
        with self.assertRaises(ValueError):
            CFG._canonise_rules(rules)
        
    def test_nonstring_symbol(self):
        rules = {'A': [[1, 'a']]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    def test_nesting_too_deep(self):
        rules = {'A': [[['a']]]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

        rules1 = {'A': [['a', []]]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules1)

        rules2 = {'A': [['a', ['b']]]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules2)

    # TODO test different container types


# NOTE _extract() is only called on rules that are already canonised and syntactically valid
class TestExtract(unittest.TestCase):

    def test_empty_cfg(self):
        rules = {}
        self.assertEqual(CFG._extract(rules), (tuple(), tuple()))

    def test_single_rule(self):
        rules = {'A': (('a',),)}
        self.assertEqual(CFG._extract(rules), (('A',), ('a',)))

    def test_multiple_rules_single_nonterminal(self):
        rules = {'A': (('a',), ('b',), ('c', 'd'))}
        self.assertEqual(CFG._extract(rules), (('A',), ('a', 'b', 'c', 'd')))

    def test_multiple_nonterminals(self):
        rules = {'A': (('a',),),
                 'B': (('b',),)}
        self.assertEqual(CFG._extract(rules), (('A', 'B'), ('a', 'b')))

    def test_nonterminal_in_body(self):
        # In body of self
        rules = {'A': (('a',), ('A',), ('b',))}
        self.assertEqual(CFG._extract(rules), (('A',), ('a', 'b')))

        # In body of other nonterminal
        rules1 = {'A': (('a',), ('b', 'c')),
                  'B': (('a', 'A'),)}
        self.assertEqual(CFG._extract(rules1), (('A', 'B'), ('a', 'b', 'c')))

    def test_sorting(self):
        rules = {'A': (('b',), ('c',), ('a',))}
        self.assertEqual(CFG._extract(rules), (('A',), ('a', 'b', 'c')))

    def test_empty_symbol_dropped(self):
        rules = {'A': (('a',), ('',))}
        self.assertEqual(CFG._extract(rules), (('A',), ('a',)))

    def test_deduplication(self):
        rules = {'A': (('a', 'b'),),
                 'B': (('b', 'c'),),
                 'C': (('c', 'a'),)}
        self.assertEqual(CFG._extract(rules), (('A', 'B', 'C'), ('a', 'b', 'c')))

    def test_no_terminals(self):
        rules = {'A': (('B',), ('B', 'A')),
                 'B': (('A',), ('B', 'A'))}
        self.assertEqual(CFG._extract(rules), (('A', 'B'), tuple()))

    def test_mixed_case(self):
        rules = {'A': (('B', 'a'), ('b', 'A'), ('c',), ('',)),
                 'B': (('A',), ('A', 'B'), ('A', 'c'))}
        self.assertEqual(CFG._extract(rules), (('A', 'B'), ('a', 'b', 'c')))



    





if __name__ == '__main__':
    unittest.main()