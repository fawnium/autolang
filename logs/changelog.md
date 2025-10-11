# Autolang changelog

## v0.1.0
Initial version of *autolang*. Includes the following features:
- DFA, NFA, PDA, TM
- `.accepts()` and `.L()` method for each automaton class
- `regex_to_nfa()` to convert regex string to NFA
- `nfa_to_dfa()` to convert NFA to DFA using subset construction

## v0.1.1
- Patched memory issue for word-generating functions in utils.py
    - `words_of_length()` and `words_to_length()` are now generators, so they only yield each word as needed instead of storing all of them in memory
    - It is still possible to return the entire tuple of words by setting the arg `lazy = False`, but this should be used with caution due to exponential memory usage, which can cause system crashes
