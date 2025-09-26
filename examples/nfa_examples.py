from autolang import NFA

'''
#### NFA EXAMPLES FROM SIPSER ####

This file shows various examples of NFAs, how to create them, and how to use them.
'''

'''
NFA N1 in Sipser, p48

The language of N1 is {w | w contains '101' or '11' as a subword}
'''
# Transition table
tran1 = {
    ('q1', '0'): ('q1',), # NOTE if there is only one next state, we need a comma inside the brackets so that it is recognised as a tuple and not a string!
    ('q1', '1'): ('q1', 'q2'), # There are 2 transitions from 'q1' when reading '1'

    ('q2', ''): ('q3',),
    ('q2', '0'): ('q3',),

    ('q3', '1'): ('q4',),

    ('q4', '0'): ('q4',),
    ('q4', '1'): ('q4',) 
}
# Create NFA itself
N1 = NFA(tran1, 'q1', ['q4'])

print('\n' * 4)
print('#### NFA N1 ####')
print(f'How N1 appears in text: {N1}')

print(f'N1 accepts "010": {N1.accepts('010')}')
print(f'N1 accepts "010110": {N1.accepts('010110')}')
print(f'N1 accepts "0011000": {N1.accepts('0011000')}')

print('Below is the language of N1 up to length 3:')
print(N1.L(3))

print('Below is the transition table of N1:')
N1.transition_table()





'''
NFA N3 in Sipser, p52

The language of N3 is {0^k | k is a multiple of 2 or 3}
'''
# Transition table
# NOTE this NFA doesn't have labelled states in the text, so here we choose to start at 'q0' (which is objectively superior to 'q1'!)
tran3 = {
    ('q0', ''): ('q1', 'q3'),
    ('q1', '0'): ('q2',),
    ('q2', '0'): ('q1',),
    ('q3', '0'): ('q4',),
    ('q4', '0'): ('q5',),
    ('q5', '0'): ('q3',)
}
# Create NFA itself
N3 = NFA(tran3, 'q0', ['q1', 'q3'])

print('\n' * 4)
print('#### NFA N3 ####')
print(f'How N3 appears in text: {N3}')

print(f'N3 accepts "0": {N3.accepts('0')}')
print(f'N3 accepts "00": {N3.accepts('00')}')
print(f'N3 accepts "000": {N3.accepts('000')}')
print(f'N3 accepts "00000": {N3.accepts('00000')}')

print('Below is the language of N3 up to length 20:')
print(N3.L(20))

print('Below is the transition table of N3:')
N3.transition_table()