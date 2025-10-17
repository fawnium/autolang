import unittest
from autolang.backend.regex.regex_input import is_valid_regex, alphabet_of, add_concat

# NOTE this class implicitly tests `RegexParserInput`, since `is_valid_regex` is just a wrapper
class TestIsValidRegex(unittest.TestCase):
    
    def test_valid(self):
        self.assertTrue(is_valid_regex('')) # Empty regex
        self.assertTrue(is_valid_regex('a')) # Single atom
        self.assertTrue(is_valid_regex('a*')) # Star
        self.assertTrue(is_valid_regex('ab')) # Concat
        self.assertTrue(is_valid_regex('a+b')) # Union
        self.assertTrue(is_valid_regex('(a+b)')) # Grouped union
        self.assertTrue(is_valid_regex('(a+b)*')) # Star applied to group
        self.assertTrue(is_valid_regex('a(b+c)')) # Concat with group
        self.assertTrue(is_valid_regex('(a+b)(b+c)')) # Concat groups
        self.assertTrue(is_valid_regex('(a)')) # Redundant brackets
        self.assertTrue(is_valid_regex('((a))')) # Nested brackets
        self.assertTrue(is_valid_regex('((a)+(b))*')) # Complex nested with star
        self.assertTrue(is_valid_regex('(a+b)(c+d)*')) # Mixed concat and star
        self.assertTrue(is_valid_regex('a*+b')) # Union after star
        self.assertTrue(is_valid_regex('a(a+b)*')) # Atom followed by star group
        self.assertTrue(is_valid_regex('a(bc)*')) # Star applied to concat group
        self.assertTrue(is_valid_regex('a+(b+c)*')) # Union and star
        self.assertTrue(is_valid_regex('a*(b+c)d')) # Concat after star
        self.assertTrue(is_valid_regex('((a+b)*c)*')) # Mixed nesting
        self.assertTrue(is_valid_regex('((a + b) * c) *')) # Same as above but with spaces

    def test_invalid(self):
        self.assertFalse(is_valid_regex('*a')) # Star without preceding atom
        self.assertFalse(is_valid_regex('+a')) # Union with missing left atom
        self.assertFalse(is_valid_regex('a+')) # Union with missing right atom
        self.assertFalse(is_valid_regex('a++b')) # Double union
        self.assertFalse(is_valid_regex('a**')) # Double star
        self.assertFalse(is_valid_regex('a(b+c')) # Missing closing bracket
        self.assertFalse(is_valid_regex('a+b)')) # Unmatched closing bracket
        self.assertFalse(is_valid_regex('(')) # Opening bracket with no expression
        self.assertFalse(is_valid_regex(')')) # Lone closing bracket
        self.assertFalse(is_valid_regex('+')) # Union with no operands
        self.assertFalse(is_valid_regex('*')) # Star with no operands
        self.assertFalse(is_valid_regex('(+)')) # Union with no operands in bracket
        self.assertFalse(is_valid_regex('(a+)')) # Trailing operator in group
        self.assertFalse(is_valid_regex('(+a)')) # Missing left operand in group
        self.assertFalse(is_valid_regex('a(()b)')) # Empty group
        self.assertFalse(is_valid_regex('a(*b)')) # Star in wrong place
        self.assertFalse(is_valid_regex('a+*b')) # Star after union
        self.assertFalse(is_valid_regex('a(b+)')) # Union with missing right atom in group
        self.assertFalse(is_valid_regex('(a+b))')) # Extra closing bracket
        self.assertFalse(is_valid_regex('((a+b)')) # Extra opening bracket
        self.assertFalse(is_valid_regex('a()b')) # Empty group in middle of expression


class TestAlphabetOf(unittest.TestCase):

    def test_alphabet_of(self):
        self.assertEqual(set(alphabet_of('')), set())
        self.assertEqual(set(alphabet_of('a')), {'a'})
        self.assertEqual(set(alphabet_of('aa')), {'a'})
        self.assertEqual(set(alphabet_of('ab')), {'a', 'b'})
        self.assertEqual(set(alphabet_of('a+a')), {'a'})
        self.assertEqual(set(alphabet_of('a+b')), {'a', 'b'})
        self.assertEqual(set(alphabet_of('a.a')), {'a'})
        self.assertEqual(set(alphabet_of('a.b')), {'a', 'b'})
        self.assertEqual(set(alphabet_of('a.b.c')), {'a', 'b', 'c'})
        self.assertEqual(set(alphabet_of('a*')), {'a'})
        self.assertEqual(set(alphabet_of('(a+c*)*.0*.(c+d+5.f)')), {'a', 'c', '0', 'd', '5', 'f'})


class TestAddConcat(unittest.TestCase):

    def test_add_concat(self):
        self.assertEqual(add_concat('a'), 'a')
        self.assertEqual(add_concat('ab'), 'a.b')
        self.assertEqual(add_concat('abc'), 'a.b.c')
        self.assertEqual(add_concat('a(b)'), 'a.(b)')
        self.assertEqual(add_concat('(a)b'), '(a).b')
        self.assertEqual(add_concat('a(bc)'), 'a.(b.c)')
        self.assertEqual(add_concat('(ab)c'), '(a.b).c')
        self.assertEqual(add_concat('a*'), 'a*')
        self.assertEqual(add_concat('a*b'), 'a*.b')
        self.assertEqual(add_concat('a*(b)'), 'a*.(b)')
        self.assertEqual(add_concat('a+b'), 'a+b')
        self.assertEqual(add_concat('a(b*c)'), 'a.(b*.c)')
        self.assertEqual(add_concat('(ab)(cd)'), '(a.b).(c.d)')
        self.assertEqual(add_concat('a*(b+c*)((a+bb)*+ab)c'), 'a*.(b+c*).((a+b.b)*+a.b).c')


if __name__ == '__main__':
    unittest.main()