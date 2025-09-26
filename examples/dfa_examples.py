from autolang import DFA
'''
#### DFA EXAMPLES FROM SIPSER ####

This file shows various examples of DFAs, how to create them, and how to use them.
'''

'''
DFA M1 in Sipser, p36

The language of the machine M1 is {w | w contains at least one '1' and the final '1' is followed by an even number of '0's}
'''

# Define transition table of DFA
# NOTE transition entries can be given in any order, but it is good practice to write them systematically as below
tran1 = {
    ('q1', '0'): 'q1',
    ('q1', '1'): 'q2',
    ('q2', '0'): 'q3',
    ('q2', '1'): 'q2',
    ('q3', '0'): 'q2',
    ('q3', '1'): 'q2'
}
# Create DFA itself
M1 = DFA(tran1, 'q1', ['q2']) # Arguments are in order: transition function, start state, list of accept states

print('\n' * 4)
print('#### DFA M1 ####')
print(f'How M1 appears in text: {M1}')

print(f'M1 accepts the word "000": {M1.accepts('000')}')
print(f'M1 accepts the word "010": {M1.accepts('010')}')
print(f'M1 accepts the word "010100": {M1.accepts('010100')}')

print('Below is the language of M1 in len-lex order, for length <= 4:')
print(M1.L(4))

print('Below is the transition table of M1:')
M1.transition_table()



'''
DFA M2 in Sipser, p37

The language of M2 is {w | w ends with a '1'}
'''

# Transition table
tran2 = {
    ('q1', '0'): 'q1',
    ('q1', '1'): 'q2',
    ('q2', '0'): 'q1',
    ('q2', '1'): 'q2'
}
# Create DFA itself
M2 = DFA(tran2, 'q1', ['q2'])

print('\n' * 4)
print('#### DFA M2 ####')
print(f'How M2 appears in text: {M2}')

print(f'M2 accepts "1101": {M2.accepts('1101')}')
print(f'M2 accepts "110": {M2.accepts('110')}')

print('Below is the language of M2 up to length 5:')
print(M2.L()) # If no length given to generate the language, the default length is 5

print('Below is the transition table of M2:')
M2.transition_table()





'''
DFA M3 in Sipser, p38

The language of M3 is {w | w is the empty string or w ends with a '0'}
NOTE that M3 can accept the empty word.
NOTE also that for this example we start with 'q0' and not 'q1', just 
to prove that the state names can be arbitrary, as long as they are consistent!
'''

# Transition table
tran3 = {
    ('q0', '0'): 'q0',
    ('q0', '1'): 'q1',
    ('q1', '0'): 'q0',
    ('q1', '1'): 'q1'
}
# Create DFA itself
M3 = DFA(tran3, 'q0', ['q0'])

print('\n' * 4)
print('#### DFA M3 ####')
print(f'How M3 appears in text: {M3}')

print(f'M3 accepts the empty word "": {M3.accepts('')}')
print(f'M3 accepts "001": {M3.accepts('001')}')
print(f'M3 accepts "110": {M3.accepts('110')}')

print('Below is the language of M3 up to length 3:')
print(M3.L(3))

print('Below is the transition table of M3:')
M3.transition_table()






'''

DFA M4 in Sipser, p38

The alphabet of M4 is {a, b}, and the language is {w | w starts and ends with the same letter}
'''

# Transition table
tran4 = {
    ('s', 'a'): 'q1',
    ('s', 'b'): 'r1',
    ('q1', 'a'): 'q1',
    ('q1', 'b'): 'q2',
    ('q2', 'a'): 'q1',
    ('q2', 'b'): 'q2',
    ('r1', 'a'): 'r2',
    ('r1', 'b'): 'r1',
    ('r2', 'a'): 'r2',
    ('r2', 'b'): 'r1'
}
# Create DFA itself
M4 = DFA(tran4, 's', {'q1', 'r1'}) # Here we use a set instead of a list to give the accept states - any valid Iterable should work!

print('\n' * 4)
print('#### DFA M4 ####')
print(f'How M4 appears in text: {M4}')

print(f'M4 accepts "ab": {M4.accepts('ab')}')
print(f'M4 accepts "abbaba": {M4.accepts('abbaba')}')
print('But how does M4 handle a word with the surprise letter "c"?')
print(f'M4 accepts "aca": {M4.accepts('aca')}')
print('As shown above, automata will always reject words that contain letters not in their alphabet.')

print('Below is the language of M4 up to length 4')
print(M4.L(4))

print('Below is the transition table of M4:')
M4.transition_table()