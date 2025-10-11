from collections.abc import Iterable, Generator
import re

'''
General utility functions for autolang
- Primarily generating words over alphabets
'''

# Maximum size of tuple of generated words before raising error to prevent memory overflow
def get_max_words_size() -> int:
    return int(1e6) # Default 1 million - should be ok on most systems
    # TODO ? use `sys` for better estimate?

# Number of words of length exactly n for given number of alphabet letters
def get_alphabet_size_single_length(n: int, len_alphabet: int) -> int:
    return len_alphabet ** n

# Number of words of length less than or equal to n for given alphabet size
def get_alphabet_size_all_lengths(n: int, len_alphabet: int) -> int:
    # Closed form sum of above function's values - geometric series
    if len_alphabet == 1: # Prevent division by zero in special case
        return n + 1 # e.g. ('', 'a', 'aa', ...)
    else:
        return (len_alphabet ** (n + 1) - 1) // (len_alphabet - 1) # Floor div to return int

# Return generator for all words of length exactly n over given alphabet
def _words_of_length_gen(n: int, alphabet: tuple[str, ...]) -> Generator[str]:
    '''
    - recursively generate all words of length n, by appending each alphabet letter to each word length n - 1
    - use `yield` to save memory with lazy evaluation
    '''
    if n < 0:
        raise ValueError('Argument \'n\' must be non-negative.')
    # Base case
    if n == 0:
        yield ''
    # Recursive case
    else:
        for word in _words_of_length_gen(n - 1, alphabet):
            for letter in alphabet:
                yield word + letter

# Public wrapper for above
# if lazy = False, returns all words as tuple in-memory
def words_of_length(n: int, alphabet: Iterable[str], lazy = True) -> Generator[str] | tuple[str, ...]:
    '''
    - convert alphabet to tuple before generating words
    - in particular ensure hashable for lru cache
        - NOTE lru cache no longer used, but ensure hashability just in case
    '''
    if n < 0:
        raise ValueError('Argument \'n\' must be non-negative.')
    # Check memory safety if returning whole tuple
    if not lazy:
        limit = get_max_words_size()
        size = get_alphabet_size_single_length(n, len(alphabet))
        if size >= limit:
            proceed = input(f'WARNING: using non-lazy word generation for {size} total words may cause system memory overflow. Proceed anyway? (Y/n): ')
            if proceed != 'Y':
                raise MemoryError('Too many words requested to generate in memory.')
            
    words = _words_of_length_gen(n, tuple(alphabet)) # Generator for words of length n
    return words if lazy else tuple(words)

# Generate all words of length less than or equal to n over given alphabet
# if lazy = False, returns all words as tuple in-memory
def words_to_length(n: int, alphabet: Iterable[str], lazy = True) -> Generator[str] | tuple[str, ...]:
    '''
    for 0 <= i <= n:
        - yield each word of length i
        - this covers all words of all lengths up to n
    - return generator, or convert to tuple if lazy = False
    '''
    if n < 0:
        raise ValueError('Argument \'n\' must be non-negative.')
    # Check memory safety if returning whole tuple
    if not lazy:
        limit = get_max_words_size()
        size = get_alphabet_size_all_lengths(n, len(alphabet))
        if size >= limit:
            proceed = input(f'WARNING: using non-lazy word generation for {size} total words may cause system memory overflow. Proceed anyway? (Y/n): ')
            if proceed != 'Y':
                raise MemoryError('Too many words requested to generate in memory.')
            
    # Generator for words of length n or less
    def _gen():
        for i in range(n + 1):
            for word in words_of_length(i, alphabet, lazy = True):
                yield word
    return _gen() if lazy else tuple(_gen())

# Return all words up to given length that match given regular expression
# Mainly for development testing, not autolang feature
def words_to_length_from_regex(n: int, alphabet: Iterable[str], regex: str, lazy = True) -> Generator[str] | tuple[str, ...]:
    # Convert formal regex to python-regex
    py_regex = regex.replace('.', '') # Remove explicit concat if present
    py_regex = py_regex.replace('+', '|') # Union has a different representation in python regex

    # Generator for words matching regex
    def _gen():
        for word in words_to_length(n, alphabet, lazy = True):
            if re.fullmatch(py_regex, word):
                yield word

    return _gen() if lazy else tuple(_gen())