import unittest
from autolang.backend.utils import words_of_length, words_to_length

class TestWordsOfLength(unittest.TestCase):

    def test_length_zero(self):
        self.assertEqual(words_of_length(0, 'ab'), ('',))

    def test_length_one(self):
        self.assertEqual(set(words_of_length(1, 'ab')), {'a', 'b'})

    def test_length_two(self):
        self.assertEqual(set(words_of_length(2, 'ab')), {'aa', 'ab', 'ba', 'bb'})

    def test_length_twelve(self):
        self.assertEqual(len(words_of_length(12, 'ab')), 2 ** 12)

    def test_from_list(self):
        self.assertEqual(set(words_of_length(1, ['a', 'b'])), {'a', 'b'})

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            words_of_length(-1, 'ab')

    def test_empty_alphabet(self):
        self.assertEqual(words_of_length(1, ''), tuple())


class TestWordsToLength(unittest.TestCase):

    def test_length_zero(self):
        self.assertEqual(words_to_length(0, 'ab'), ('',))

    def test_length_one(self):
        self.assertEqual(set(words_to_length(1, 'ab')), {'', 'a', 'b'})

    def test_length_two(self):
        self.assertEqual(set(words_to_length(2, 'ab')), {'', 'a', 'b', 'aa', 'ab', 'ba', 'bb'})

    def test_from_list(self):
        self.assertEqual(set(words_to_length(1, ['a', 'b'])), {'', 'a', 'b'})

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            words_to_length(-1, 'ab')

    def test_empty_alphabet(self):
        self.assertEqual(words_to_length(1, ''), ('',))


class TestWordsToLengthFromRegex(unittest.TestCase):
    # This func is essentially native python, so I think testing it is somewhat circular
    pass


if __name__ == '__main__':
    unittest.main()