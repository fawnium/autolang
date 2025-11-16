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
    def test_empty_body(self):
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

    def test_bodies_not_iterable(self):
        rules = {'A': 1}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

    def test_body_not_sequence(self):
        # Body not even container
        rules = {'A': [1]}
        with self.assertRaises(TypeError):
            CFG._canonise_rules(rules)

        # Body container but not ordered
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


class TestRenameSymbols(unittest.TestCase):

    pass # TODO only after method has been rewritten


class TestUnion(unittest.TestCase):

    pass # TODO along with _rename_symbols


class TestDeleteBodyFromBodies(unittest.TestCase):

    def test_missing_target(self):
        bodies = (('a',), ('b',), ('c',))
        target = ('d',)
        with self.assertRaises(ValueError):
            CFG._delete_body_from_bodies(target, bodies)

    def test_present_target(self):
        bodies = (('a',), ('b',), ('c',))
        self.assertEqual(CFG._delete_body_from_bodies(('a',), bodies), (('b',), ('c',)))
        self.assertEqual(CFG._delete_body_from_bodies(('b',), bodies), (('a',), ('c',)))
        self.assertEqual(CFG._delete_body_from_bodies(('c',), bodies), (('a',), ('b',)))


class TestFilterBodies(unittest.TestCase):

    pass # TODO


class TestGetBodiesContaining(unittest.TestCase):

    def test_single_nonterminal(self):
        # As unit rule
        rules = {'A': (('a',), ('A',))}
        self.assertEqual(CFG._get_bodies_containing('A', rules), {'A': (('A',),)})

        # As compound rule, one occurrence per rule
        rules1 = {'A': (('a',), ('a', 'A'), ('A', 'b', 'a'))}
        self.assertEqual(CFG._get_bodies_containing('A', rules1), {'A': (('a', 'A'), ('A', 'b', 'a'))})

        # As compound, multiple occurrences per rule
        rules2 = {'A': (('a',), ('A', 'A'), ('A', 'a', 'A'), ('A',), ('',))}
        self.assertEqual(CFG._get_bodies_containing('A', rules2), {'A': (('A', 'A'), ('A', 'a', 'A'), ('A',))})

    def test_multiple_nonterminals(self):
        # Only one occurrence of each nonterminal per rule - multiple should be covered in above
        rules = {'A': (('a',), ('a', 'A'), ('B', 'a', 'A'), ('C',)),
                 'B': (('',), ('B', 'a'), ('A', 'a'), ('a', 'C')),
                 'C': (('a', 'A', 'B'), ('',), ('C', 'a'), ('a', 'A'))}
        
        expected_A = {'A': (('a', 'A'), ('B', 'a', 'A')),
                      'B': (('A', 'a'),),
                      'C': (('a', 'A', 'B'), ('a', 'A'))}
        expected_B = {'A': (('B', 'a', 'A'),),
                      'B': (('B', 'a'),),
                      'C': (('a', 'A', 'B'),)}
        expected_C = {'A': (('C',),),
                      'B': (('a', 'C'),),
                      'C': (('C', 'a'),)}
        self.assertEqual(CFG._get_bodies_containing('A', rules), expected_A)
        self.assertEqual(CFG._get_bodies_containing('B', rules), expected_B)
        self.assertEqual(CFG._get_bodies_containing('C', rules), expected_C)

class TestGetBodiesOfLength(unittest.TestCase):
    
    pass # TODO


class TestGetBodiesLengthGreaterThan(unittest.TestCase):

    pass # TODO


class TestAddNewRules(unittest.TestCase):

    def test_single_rule(self):
        initial_rules = {'A': (('a',), ('b',))}
        new_rules = {'A': (('c',),)}
        self.assertEqual(CFG._add_new_rules(new_rules, initial_rules), {'A': (('a',), ('b',), ('c',))})

    def test_multiple_rules(self):
        initial_rules = {'A': (('a',), ('b',))}
        new_rules = {'A': (('c',), ('d',))}
        self.assertEqual(CFG._add_new_rules(new_rules, initial_rules), {'A': (('a',), ('b',), ('c',), ('d',))})

    def test_deduplication(self):
        initial_rules = {'A': (('a',), ('b',))}
        new_rules = {'A': (('a',),)}
        self.assertEqual(CFG._add_new_rules(new_rules, initial_rules), {'A': (('a',), ('b',))})

    def test_multiple_nonterminals(self):
        initial_rules = {'A': (('a',), ('b',)),
                         'B': (('c',), ('d',)),
                         'C': (('e',), ('f',))}
        # None added for 'C'
        new_rules = {'A': (('x',),),
                     'B': (('y',),)}
        self.assertEqual(CFG._add_new_rules(new_rules, initial_rules), {'A': (('a',), ('b',), ('x',)), 
                                                                        'B': (('c',), ('d',), ('y',)),
                                                                        'C': (('e',), ('f',))})

    # New nonterminals added via .add_new_nonterminals()
    def test_invalid_nonterminal(self):
        initial_rules = {'A': (('a',), ('b',))}
        new_rules = {'X': (('c',),)}
        with self.assertRaises(ValueError):
            CFG._add_new_rules(new_rules, initial_rules)


class TestAddNewNonterminals(unittest.TestCase):

    def test_single_new_nonterminal(self):
        initial_rules = {'A': (('a',),)}
        new_rules = {'B': (('a',),)}
        self.assertEqual(CFG._add_new_nonterminals(new_rules, initial_rules), {'A': (('a',),),
                                                                               'B': (('a',),)})

    def test_multiple_new_nonterminals(self):
        initial_rules = {'A': (('a',),)}
        new_rules = {'B': (('a',),),
                     'C': (('a',),)}
        self.assertEqual(CFG._add_new_nonterminals(new_rules, initial_rules), {'A': (('a',),),
                                                                               'B': (('a',),),
                                                                               'C': (('a',),)})
        
    def test_existing_terminal_in_body(self):
        initial_rules = {'A': (('a',),)}
        new_rules = {'B': (('a',), ('A', 'a'))}
        self.assertEqual(CFG._add_new_nonterminals(new_rules, initial_rules), {'A': (('a',),),
                                                                               'B': (('a',), ('A', 'a'))})

    def test_new_terminal_in_body(self):
        initial_rules = {'A': (('a',),)}
        new_rules = {'B': (('a',), ('B', 'a'))}
        self.assertEqual(CFG._add_new_nonterminals(new_rules, initial_rules), {'A': (('a',),),
                                                                               'B': (('a',), ('B', 'a'))})

    def test_invalid_new_nonterminal(self):
        initial_rules = {'A': (('a', 'b'),)}
        new_rules1 = {'A': (('b',),)} # Collides with existing nonterminal
        new_rules2 = {'a': (('b',),)} # Collides with existing terminal
        with self.assertRaises(ValueError):
            CFG._add_new_nonterminals(new_rules1, initial_rules)
        with self.assertRaises(ValueError):
            CFG._add_new_nonterminals(new_rules2, initial_rules)

    def test_invalid_new_terminal(self):
        initial_rules = {'A': (('a',),)}
        new_rules = {'B': (('A', 'a', 'x'))} # 'A' and 'a' ok, 'x' invalid
        with self.assertRaises(ValueError):
            CFG._add_new_nonterminals(new_rules, initial_rules)


class TestRemoveOccurrencesOf(unittest.TestCase):

    # NOTE 0 occurrences not tested as method won't be called

    def test_one_occurrence(self):
        self.assertEqual(CFG._remove_occurrences_of('A', ('u', 'A', 'v')), (('u', 'v'),)) # Prefix and suffix
        self.assertEqual(CFG._remove_occurrences_of('A', ('A', 'v')), (('v',),)) # No prefix
        self.assertEqual(CFG._remove_occurrences_of('A', ('u', 'A')), (('u',),)) # No suffix
        # NOTE in isolated case ('A',) method won't be called

    def test_two_occurrences(self):
        initial = ('u', 'A', 'v', 'A', 'w')
        expected = (('u', 'v', 'A', 'w'), ('u', 'A', 'v', 'w'), ('u', 'v', 'w'))
        self.assertEqual(set(CFG._remove_occurrences_of('A', initial)), set(expected))

    def test_three_occurrences(self):
        initial = ('u', 'A', 'v', 'A', 'w', 'A', 'x')
        expected = (('u', 'v', 'A', 'w', 'A', 'x'), ('u', 'A', 'v', 'w', 'A', 'x'), ('u', 'A', 'v', 'A', 'w', 'x'),
                    ('u', 'v', 'w', 'A', 'x'), ('u', 'v', 'A', 'w', 'x'), ('u', 'A', 'v', 'w', 'x'),
                    ('u', 'v', 'w', 'x'))
        self.assertEqual(set(CFG._remove_occurrences_of('A', initial)), set(expected))


class TestRemoveBadEpsilonRules(unittest.TestCase):

    # NOTE changing the order of rule bodies in tuple may fail tests
    # even though the grammar would still be correct

    def test_no_erules(self):
        rules = {'S': (('A',), ('B',)),
                 'A': (('a',),),
                 'B': (('b',),)}
        expected = rules
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

    def test_good_erule(self):
        rules = {'S': (('',), ('A',)),
                 'A': (('a',), ('a', 'A'))}
        expected = rules
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

    def test_single_bad_erule(self):
        # Only one rule for bad nonterminal
        rules = {'S': (('A',), ('B',)),
                 'A': (('',),),
                 'B': (('b',),)}
        expected = {'S': (('',), ('A',), ('B',)),
                    'A': tuple(),
                    'B': (('b',),)}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

        # Additional rules for bad nonterminal
        rules1 = {'S': (('A',), ('B',)),
                 'A': (('',), ('b',)),
                 'B': (('b',),)}
        expected1 = {'S': (('',), ('A',), ('B',)),
                    'A': (('b',),),
                    'B': (('b',),)}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules1, 'S'), expected1)

    # Multiple rules with bad nonterminal, one occurrence per rule
    def test_single_bad_erule_different_occurrences(self):
        rules = {'S': (('A',), ('B',),),
                 'A': (('',),),
                 'B': (('b',), ('b', 'A'), ('A', 'c'))} # New rule ('b',) should be deduplicated
        expected = {'S': (('',), ('A',), ('B',)),
                    'A': tuple(),
                    'B': (('b',), ('c',), ('A', 'c'), ('b', 'A'))}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

    # Single rule with bad nonterminal, multiple occurences in rule
    def test_single_bad_erule_multiple_occurrences(self):
        rules = {'S': (('u', 'A', 'v', 'A', 'w'),),
                 'A': (('',),)}
        expected = {'S': (('u', 'v', 'w'), ('u', 'A', 'v', 'w'), 
                          ('u', 'v', 'A', 'w'), ('u', 'A', 'v', 'A', 'w')),
                    'A': tuple()}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

    # Bad nonterminal yields itself
    def test_single_bad_erule_self_occurrence(self):
        # Self-yield is compound rule
        rules = {'S': (('A',), ('a',)),
                 'A': (('',), ('A', 'a'))}
        expected = {'S': (('',), ('A',), ('a',)),
                    'A': (('a',), ('A', 'a'))}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

        # Self-yield is unit rule
        rules1 = {'S': (('A',), ('a',)),
                 'A': (('',), ('A',), ('a',))}
        # Bad erule not re-added: 'A -> A' should induce 'A -> ε', but was already removed
        expected1 = {'S': (('',), ('A',), ('a',)),
                    'A': (('A',), ('a',),)} 
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules1, 'S'), expected1)

    def test_recursive_remove(self):
        rules = {'S': (('A',),),
                 'A': (('B',),),
                 'B': (('C',),),
                 'C': (('',), ('c',))}
        expected = {'S': (('',), ('A',)),
                    'A': (('B',),),
                    'B': (('C',),),
                    'C': (('c',),)}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

    def test_removed_not_readded(self):
        # If 'B -> ε' removed first, shouldn't be re-added when 'A -> ε' removed, and vice versa
        rules = {'S': (('A',), ('B',)),
                 'A': (('',), ('B',), ('a',)),
                 'B': (('',), ('A',), ('b',))}
        expected = {'S': (('',), ('A',), ('B',)),
                    'A': (('B',), ('a',)),
                    'B': (('A',), ('b',))}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)

    def test_multiple_bad_erules(self):
        rules = {'S': (('A',), ('B', 'C')),
                 'A': (('',), ('a',), ('a', 'b'), ('a', 'B')),
                 'B': (('',), ('C', 'b'), ('A',)),
                 'C': (('',), ('A', 'B'), ('c',))}
        expected = {'S': (('',), ('A',), ('B',), ('C',), ('B', 'C')),
                    'A': (('a',), ('a', 'B'), ('a', 'b')),
                    'B': (('A',), ('b',), ('C', 'b')),
                    'C': (('A',), ('B',), ('c',), ('A', 'B'))}
        self.assertEqual(CFG.remove_bad_epsilon_rules(rules, 'S'), expected)


class TestRemoveUnitRules(unittest.TestCase):

    # NOTE changing the order of rule bodies in tuple may fail tests
    # even though the grammar would still be correct

    # NOTE epsilon rules should not be present

    def test_no_unit_rules(self):
        rules = {'S': (('A', 'B'), ('a', 'b')),
                 'A': (('A', 'S'), ('a', 'b')),
                 'B': (('B', 'S'), ('b', 'a'))}
        expected = rules
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

    def test_terminal_not_unit(self):
        rules = {'S': (('A', 'B'),),
                 'A': (('b',), ('B',)), # A -> B should be removed, A -> b should not
                 'B': (('a', 'b'),)}
        expected = {'S': (('A', 'B'),),
                    'A': (('b',), ('a', 'b')),
                    'B': (('a', 'b'),)}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

    def test_single_unit_rule(self):
        rules = {'S': (('A',),),
                 'A': (('a',), ('a', 'b'))}
        expected = {'S': (('a',), ('a', 'b')),
                    'A': (('a',), ('a', 'b'))}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

    def test_multiple_unit_rules_same_head(self):
        rules = {'S': (('A',), ('B',)),
                 'A': (('a',), ('a', 'b')),
                 'B': (('c',), ('c', 'd'))}
        expected = {'S': (('a',), ('c',), ('a', 'b'), ('c', 'd')),
                    'A': (('a',), ('a', 'b')),
                    'B': (('c',), ('c', 'd'))}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

    def test_multiple_unit_rules_different_heads(self):
        # Same body for each occurrence
        rules = {'S': (('A', 'B'), ('A', 'C')),
                 'A': (('a',), ('C',)),
                 'B': (('b',), ('C',)),
                 'C': (('c',), ('a', 'b', 'c'))}
        expected = {'S': (('A', 'B'), ('A', 'C')),
                    'A': (('a',), ('c',), ('a', 'b', 'c')),
                    'B': (('b',), ('c',), ('a', 'b', 'c')),
                    'C': (('c',), ('a', 'b', 'c'))}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

        # Different body for each occurrence
        rules1 = {'S': (('A', 'B'), ('A', 'C')),
                  'A': (('a',), ('C',)),
                  'B': (('b',), ('D',)),
                  'C': (('c',), ('a', 'c')),
                  'D': (('d',), ('b', 'd'))}
        expected1 = {'S': (('A', 'B'), ('A', 'C')),
                     'A': (('a',), ('c',), ('a', 'c')),
                     'B': (('b',), ('d',), ('b', 'd')),
                     'C': (('c',), ('a', 'c')),
                     'D': (('d',), ('b', 'd'))}
        self.assertEqual(CFG.remove_unit_rules(rules1), expected1)

    def test_single_unit_rule_self_head(self):
        rules = {'S': (('a',), ('A', 'A')),
                 'A': (('a', 'b'), ('A',))}
        expected = {'S': (('a',), ('A', 'A')),
                    'A': (('a', 'b'),)} # Self-unit should just be removed
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

    def test_removed_not_readded(self):
        rules = {'A': (('a',), ('B',), ('C',)),
                 'B': (('b',), ('C',)),
                 'C': (('c',), ('B',))}
        expected = {'A': (('a',), ('b',), ('c',)),
                    'B': (('b',), ('c',)),
                    'C': (('b',), ('c',))}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)
        
    def test_cyclic_removal(self):
        rules = {'A': (('a',), ('B',)),
                 'B': (('b',), ('C',)),
                 'C': (('c',), ('A',)),}
        expected = {'A': (('a',), ('b',), ('c',)),
                    'B': (('a',), ('b',), ('c',)),
                    'C': (('a',), ('b',), ('c',))}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

    def test_recursive_removal(self):
        rules = {'S': (('a',), ('A',)),
                 'A': (('b',), ('B',)),
                 'B': (('c',), ('C',),),
                 'C': (('a', 'b', 'c'),)}
        expected = {'S': (('a',), ('b',), ('c',), ('a', 'b', 'c')),
                    'A': (('b',), ('c',), ('a', 'b', 'c')),
                    'B': (('c',), ('a', 'b', 'c')),
                    'C': (('a', 'b', 'c'),)}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)

    def test_deduplication(self):
        rules = {'S': (('A',), ('a', 'b')),
                 'A': (('a',), ('a', 'b'))} # ('a', 'b') already rule for S
        expected = {'S': (('a',), ('a', 'b')),
                    'A': (('a',), ('a', 'b'))}
        self.assertEqual(CFG.remove_unit_rules(rules), expected)


class TestRemoveRulesBodyLengthGreaterThan2(unittest.TestCase):

    pass # TODO






class TestIsChomskyNormalForm(unittest.TestCase):

    def test_true(self):
        rules = {'S': (('',), ('a',), ('A', 'B'), ('A', 'C')),
                 'A': (('a',), ('A', 'B')),
                 'B': (('b',), ('A', 'C'), ('B', 'C')),
                 'C': (('a',), ('B', 'A'), ('B', 'B'))}
        self.assertTrue(CFG._is_chomsky_normal_form(rules, 'S'))

    def test_false_terminal_in_compound(self):
        rules = {'S': (('a',), ('A', 'A')),
                 'A': (('a', 'A'))}
        self.assertFalse(CFG._is_chomsky_normal_form(rules, 'S'))

    def test_false_unit_nonterminal(self):
        rules = {'S': (('A',),),
                 'A': (('a',), ('A', 'A'))}
        self.assertFalse(CFG._is_chomsky_normal_form(rules, 'S'))

    def test_false_too_many_nonterminals(self):
        rules = {'S': (('a',), ('A', 'B'),),
                 'A': (('a',), ('A', 'B', 'A')),
                 'B': (('b',),)}
        self.assertFalse(CFG._is_chomsky_normal_form(rules, 'S'))

    def test_false_bad_erule(self):
        rules = {'S': (('a',), ('A', 'A')),
                 'A': (('',), ('a',), ('A', 'A'))}
        self.assertFalse(CFG._is_chomsky_normal_form(rules, 'S'))

    def test_false_start_in_body(self):
        rules = {'S': (('',), ('A', 'A')),
                 'A': (('a',), ('A', 'S'))}
        self.assertFalse(CFG._is_chomsky_normal_form(rules, 'S'))
    

if __name__ == '__main__':
    unittest.main()