from autolang import PDA

'''
#### PDA EXAMPLES FROM SIPSER ####

This file shows various examples of PDAs, how to create them, and how to use them.
'''

'''
PDA M1 in Sipser, p114

M1 recognises the language {0^n 1^n | n >= 0}
'''
# Transition table
tran1 = {
    ('q1', '', ''): (('q2', '$'),), # NOTE the (next_state, stack_push) tuple must be wrapped in a parent tuple!

    ('q2', '0', ''): (('q2', '0'),),
    ('q2', '1', '0'): (('q3', ''),),

    ('q3', '1', '0'): (('q3', ''),),
    ('q3', '', '$'): (('q4', ''),)
}
# Create PDA itself
M1 = PDA(tran1, 'q1', ['q1', 'q4'])

print('\n' * 4)
print('#### PDA M1 ####')
print(f'How M1 appears in text: {M1}')

print(f'M1 accepts "01": {M1.accepts('01')}')
print(f'M1 accepts "011": {M1.accepts('011')}')
print(f'M1 accepts "00001111": {M1.accepts('00001111')}')

print('Below is the language of M1 up to length 10:')
print(M1.L(10))

print('Below is the transition table of M1:')
M1.transition_table()





'''
PDA M2 in Sipser, p116

M2 recognises the language {a^i b^j c^k | i,j,k >= 0 and i = j or i = k}
'''
# Transition table
tran2 = {
    ('q1', '', ''): (('q2', '$'),),

    ('q2', 'a', ''): (('q2', 'a'),),
    ('q2', '', ''): (('q3', ''), ('q5', '')),

    ('q3', '', '$'): (('q4', ''),),
    ('q3', 'b', 'a'): (('q3', ''),),

    ('q4', 'c', ''): (('q4', ''),),

    ('q5', '', ''): (('q6', ''),),
    ('q5', 'b', ''): (('q5', ''),),

    ('q6', '', '$'): (('q7', ''),),
    ('q6', 'c', 'a'): (('q6', ''),)
}
# Create PDA itself
M2 = PDA(tran2, 'q1', ['q4', 'q7'])

print('\n' * 4)
print('#### PDA M2 ####')
print(f'How M2 appears in text: {M2}')

print(f'M2 accepts the empty word "": {M2.accepts('')}')
print(f'M2 accepts "abc": {M2.accepts('abc')}')
print(f'M2 accepts "abbccc": {M2.accepts('abbccc')}')
print(f'M2 accepts "aaaabcccc": {M2.accepts('aaaabcccc')}')

print('Below is the language of M2 up to length 8:')
print(M2.L(8))

print('Below is the transition table of M2:')
M2.transition_table()





'''
PDA M3 in Sipser, p116

M3 recognises the language {w w^R | w ∈ {0, 1}* where w^R reverses the letters of w}
'''
# Transition table
tran3 = {
    ('q1', '', ''): (('q2', '$'),),

    ('q2', '0', ''): (('q2', '0'),),
    ('q2', '1', ''): (('q2', '1'),),
    ('q2', '', ''): (('q3', ''),),

    ('q3', '0', '0'): (('q3', ''),),
    ('q3', '1', '1'): (('q3', ''),),
    ('q3', '', '$'): (('q4', ''),)
}
# Create PDA itself
M3 = PDA(tran3, 'q1', ['q4'])

print('\n' * 4)
print('#### PDA M3 ####')
print(f'How M3 appears in text: {M3}')

print(f'M3 accepts "0101": {M3.accepts('0101')}')
print(f'M3 accepts "0110": {M3.accepts('0110')}')

print('Below is the language of M3 up to length 8:')
print(M3.L(8))

print('Below is the transition table of M3:')
M3.transition_table()