from functools import lru_cache
from collections.abc import Iterable
import re

'''
General utility functions for autolang
- Primarily generating words over alphabets
'''

# Return tuple of all words of length exactly `n` over given `alphabet`
@lru_cache(maxsize=None)
def _words_of_length(n: int, alphabet: tuple[str, ...]) -> tuple[str, ...]:
    '''
    - create list of words of length n, using list of words of length n-1
    - if n is zero, simply return empty word list
    - if n is nonzero, for each word of length n-1 and for each letter in alphabet, concatenate word and letter to make word of 
      length n
    - add new word to list
    '''
    if n < 0:
        raise ValueError('Argument \'n\' must be non-negative.')
    # Base case
    if n == 0:
        return ('',)
    # Recursive case
    return tuple(word + letter for word in _words_of_length(n - 1, alphabet) for letter in alphabet)

# Public wrapper for above
def words_of_length(n: int, alphabet: Iterable[str]) -> tuple[str, ...]:
    '''
    - ensure alphabet is hashable before entering recursion
    '''
    if n < 0:
        raise ValueError('Argument \'n\' must be non-negative.')
    return _words_of_length(n, tuple(alphabet))

# Return tuple of all words of length less than or equal to `n` over given `alphabet`
def words_to_length(n: int, alphabet: Iterable[str]) -> tuple[str, ...]:
    '''
    - for all 0 <= i <= n, add words of length i to result, then return
    '''
    if n < 0:
        raise ValueError('Argument \'n\' must be non-negative.')
    words = []
    for i in range(n + 1):
        words += words_of_length(i, alphabet)
    return tuple(words)

# Return all words up to given length that match given regular expression
def words_to_length_from_regex(n: int, alphabet: Iterable, regex: str) -> tuple[str, ...]:
    # Convert formal regex to python-regex
    py_regex = regex.replace('.', '') # Remove explicit concat if present
    py_regex = py_regex.replace('+', '|') # Union has a different representation in python regex
    return tuple(word for word in words_to_length(n, alphabet) if re.fullmatch(py_regex, word))