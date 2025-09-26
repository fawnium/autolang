from autolang import regex_to_nfa, nfa_to_dfa

'''
#### CONVERTING REGULAR EXPRESSIONS TO NFAs and DFAs ####

This file shows how to convert various regular expression strings into the corresponding automata.

NOTE in *autolang*, union is '+' (NOT '|'), star is '*', and concatenation is '.' where explicit

If `R` is a string representing a regular expression, then `R` can be converted to an NFA and 
subsequently a DFA as follows:

R_nfa = regex_to_nfa(R)
R_dfa = nfa_to_dfa(R_nfa) 

- All examples are taken from Sipser, Section 1.3
- These examples are intended to demonstrate that the DFAs and NFAs constructed from the respective 
regex recognise the correct languages.
- This can be seen by manually inspecting the languages and checking they match the regex.
- Alternatively, a more rigorous comparison can be made using `words_to_length_from_regex()` in 
`autolang.backend.utils.py`, which uses the python `re` module.
'''

# Example 1 - {w | w starts with '0' or '1' followed by zero or more '0's}
# Define regex
regex1 = '(0+1)0*'
print('\n' * 4)
print(f'Input regex: {regex1}')

# Construct NFA
nfa1 = regex_to_nfa(regex1)
print(f'Language of corresponding NFA {nfa1}:')
print(nfa1.L(10))

# Construct DFA
dfa1 = nfa_to_dfa(nfa1)
print(f'Language of corresponding DFA {dfa1}:')
print(dfa1.L(10))
print('')




# Example 2 - {w | w contains exactly one '1'}
# Define regex
regex2 = '0*10*'
print('\n' * 4)
print(f'Input regex: {regex2}')

# Construct NFA
nfa2 = regex_to_nfa(regex2)
print(f'Language of corresponding NFA {nfa2}:')
print(nfa2.L())

# Construct DFA
dfa2 = nfa_to_dfa(nfa2)
print(f'Language of corresponding DFA {dfa2}:')
print(dfa2.L())




# Example 3 - {w | w contains at least one '1'}
# Define regex
regex3 = '(0+1)*1(0+1)*'
print('\n' * 4)
print(f'Input regex: {regex3}')

# Construct NFA
nfa3 = regex_to_nfa(regex3)
print(f'Language of corresponding NFA {nfa3}:')
print(nfa3.L(4))

# Construct DFA
dfa3 = nfa_to_dfa(nfa3)
print(f'Language of corresponding DFA {dfa3}:')
print(dfa3.L(4))




# Example 4 - {w | w contains '001' as a subword}
# Define regex
regex4 = '(0+1)*001(0+1)*'
print('\n' * 4)
print(f'Input regex: {regex4}')

# Construct NFA
nfa4 = regex_to_nfa(regex4)
print(f'Language of corresponding NFA {nfa4}:')
print(nfa4.L(5))

# Construct DFA
dfa4 = nfa_to_dfa(nfa4)
print(f'Language of corresponding DFA {dfa4}:')
print(dfa4.L(5))




# Example 5 - {w | w has even length}
# Define regex
regex5 = '((0+1)(0+1))*'
print('\n' * 4)
print(f'Input regex: {regex5}')

# Construct NFA
nfa5 = regex_to_nfa(regex5)
print(f'Language of corresponding NFA {nfa5}:')
print(nfa5.L(4))

# Construct DFA
dfa5 = nfa_to_dfa(nfa5)
print(f'Language of corresponding DFA {dfa5}:')
print(dfa5.L(4))




# Example 6 - {01, 10}
# Define regex
regex6 = '01+10'
print('\n' * 4)
print(f'Input regex: {regex6}')

# Construct NFA
nfa6 = regex_to_nfa(regex6)
print(f'Language of corresponding NFA {nfa6}:')
print(nfa6.L(4))

# Construct DFA
dfa6 = nfa_to_dfa(nfa6)
print(f'Language of corresponding DFA {dfa6}:')
print(dfa6.L(4))




# Example 7 - example 1.56 in Sipser, p68
# Define regex
regex7 = '(ab+a)*'
print('\n' * 4)
print(f'Input regex: {regex7}')

# Construct NFA
nfa7 = regex_to_nfa(regex7)
print(f'Language of corresponding NFA {nfa7}:')
print(nfa7.L(6))

# Construct DFA
dfa7 = nfa_to_dfa(nfa7)
print(f'Language of corresponding DFA {dfa7}:')
print(dfa7.L(6))
