import unittest
from autolang.backend.regex.regex_eliminate import RegexParserEliminate

class TestRegexParserEliminate(unittest.TestCase):

    def test_trim_enclosing_brackets(self):
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets(''), '')
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets('a'), 'a')
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets('(a)'), 'a')
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets('((a))'), 'a')
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets('(((a)))'), 'a')
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets('(a)(b)'), '(a)(b)')
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets('((a)(b))'), '(a)(b)')
        self.assertEqual(RegexParserEliminate.trim_enclosing_brackets('()'), '')

    def test_parse(self):
        self.assertEqual(RegexParserEliminate.parse(''), ('primitive', tuple()))
        self.assertEqual(RegexParserEliminate.parse('()'), ('primitive', tuple()))
        self.assertEqual(RegexParserEliminate.parse('a'), ('primitive', tuple()))
        self.assertEqual(RegexParserEliminate.parse('(a)'), ('primitive', tuple()))
        self.assertEqual(RegexParserEliminate.parse('a+b'), ('union', ('a', 'b')))
        self.assertEqual(RegexParserEliminate.parse('a.b'), ('concat', ('a', 'b')))
        self.assertEqual(RegexParserEliminate.parse('a*'), ('star', ('a',)))
        self.assertEqual(RegexParserEliminate.parse('(a*)'), ('star', ('a',)))
        self.assertEqual(RegexParserEliminate.parse('(a)*'), ('star', ('(a)',)))
        self.assertEqual(RegexParserEliminate.parse('((a)*)'), ('star', ('(a)',)))
        self.assertEqual(RegexParserEliminate.parse('a.b+c'), ('union', ('a.b', 'c')))
        self.assertEqual(RegexParserEliminate.parse('a.(b+c)'), ('concat', ('a', '(b+c)')))
        self.assertEqual(RegexParserEliminate.parse('a.(b+c)*'), ('concat', ('a', '(b+c)*')))
        self.assertEqual(RegexParserEliminate.parse('(a.b)+(c.d)'), ('union', ('(a.b)', '(c.d)')))
        self.assertEqual(RegexParserEliminate.parse('a*.b*'), ('concat', ('a*', 'b*')))
        self.assertEqual(RegexParserEliminate.parse('(a.b)*'), ('star', ('(a.b)',)))
        self.assertEqual(RegexParserEliminate.parse('(a+b)*'), ('star', ('(a+b)',)))
        self.assertEqual(RegexParserEliminate.parse('a+b+c'), ('union', ('a', 'b+c')))
        self.assertEqual(RegexParserEliminate.parse('(a+b).c*'), ('concat', ('(a+b)', 'c*')))
        self.assertEqual(RegexParserEliminate.parse('(a+b)*.c'), ('concat', ('(a+b)*', 'c')))


if __name__ == '__main__':
    unittest.main()