from collections.abc import Iterable, Generator, Container, Callable
from typing import Any
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
def get_num_words_of_length(n: int, len_alphabet: int) -> int:
    return len_alphabet ** n

# Number of words of length less than or equal to n for given alphabet size
def get_num_words_to_length(n: int, len_alphabet: int) -> int:
    # Closed form sum of above function's values - geometric series
    if len_alphabet == 1: # Prevent division by zero in special case
        return n + 1 # e.g. ('', 'a', 'aa', ...)
    else:
        return (len_alphabet ** (n + 1) - 1) // (len_alphabet - 1) # Floor div to return int
    
# Helper to halt program in case of potential memory overflow
def words_memory_safeguard(num_words: int):
    limit = get_max_words_size()
    if num_words >= limit:
        proceed = input(f'WARNING: using non-lazy word generation for {num_words} total words may cause system memory overflow. Proceed anyway? (Y/n): ')
        if proceed != 'Y':
            raise MemoryError('Too many words requested to generate in memory.')


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
def words_of_length(n: int, alphabet: Iterable[str], lazy: bool = True) -> Generator[str] | tuple[str, ...]:
    '''
    - convert alphabet to tuple before generating words
    - in particular ensure hashable for lru cache
        - NOTE lru cache no longer used, but ensure hashability just in case
    '''
    if n < 0:
        raise ValueError('Argument \'n\' must be non-negative.')
    # Check memory safety if returning whole tuple
    if not lazy:
        words_memory_safeguard(get_num_words_of_length(n, len(alphabet)))

    words = _words_of_length_gen(n, tuple(alphabet)) # Generator for words of length n
    return words if lazy else tuple(words)

# Generate all words of length less than or equal to n over given alphabet
# if lazy = False, returns all words as tuple in-memory
def words_to_length(n: int, alphabet: Iterable[str], lazy: bool = True) -> Generator[str] | tuple[str, ...]:
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
        words_memory_safeguard(get_num_words_to_length(n, len(alphabet)))
      
    # Generator for words of length n or less
    def _gen():
        for i in range(n + 1):
            for word in words_of_length(i, alphabet, lazy = True):
                yield word
    return _gen() if lazy else tuple(_gen())

# Return all words up to given length that match given regular expression
# Mainly for development testing, not autolang feature
def words_to_length_from_regex(n: int, 
                               alphabet: Iterable[str], 
                               regex: str, 
                               lazy: bool = True) -> Generator[str] | tuple[str, ...]:
    # Convert formal regex to python-regex
    py_regex = regex.replace('.', '') # Remove explicit concat if present
    py_regex = py_regex.replace('+', '|') # Union has a different representation in python regex

    # Generator for words matching regex
    def _gen():
        for word in words_to_length(n, alphabet, lazy = True):
            if re.fullmatch(py_regex, word):
                yield word

    return _gen() if lazy else tuple(_gen())


# Return string disjoint from given collection of strings
def disjoint_symbol(target: str, 
                    collection: Container[str],
                    rename_map: Callable[[str], str] = lambda s: s + '_0') -> str:
    '''
    - `target`: intended string to return
    - `collection`: collection of strings which target must not intersect with
    - `rename_map`: specifies how to rename target to make it disjoint
        - should only make minimal changes to preserve semantics

    - If target is already not in collection, return target
    - Else rename target until not in collection, then return
    '''
    if target not in collection:
        return target
    seen = {target}
    while True:
        target = rename_map(target)
        if target in seen:
            raise RecursionError(f'Renaming produced repeated string \'{target}\', cannot find disjoint name.')
        if target not in collection:
            return target
        seen.add(target)

# Determine if two collections of strings have non-empty intersection
def is_collision(collection1: Container[str], 
                 collection2: Container[str]) -> bool:
    for s in collection1:
        if s in collection2:
            return True
    for s in collection2:
        if s in collection1:
            return True
    return False

# Helper to to append entry to a value of a dict
# NOTE modifies dict in-place, so return is not used
def _append_dict_value(key: Any, 
                      entry: Any, 
                      dic: dict[Any, list[Any]]) -> dict[Any, list[Any]]:
    '''
    - If key exists in dic, append entry to it
    - If key doesn't exist, initialise it with new list [entry]
    '''
    if key in dic:
        dic[key].append(entry)
    else:
        dic[key] = [entry]
    return dic

    