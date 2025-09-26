from autolang import TM

'''
#### TM EXAMPLES FROM SIPSER ####

This file shows various examples of TMs, how to create them, and how to use them.
'''

'''
Turing Machine M1 in Sipser, p173

M1 recognises the language {w#w | w ∈ {0, 1}*}
'''
# Transition table
tran1 = {
    ('q1', '#'): ('q8', '#', 'R'),
    ('q1', '0'): ('q2', 'x', 'R'),
    ('q1', '1'): ('q3', 'x', 'R'),
    ('q1', '_'): ('qr', '_', 'R'), # NOTE since this transition goes to the reject state, it could've been omitted from dict
    ('q1', 'x'): ('qr', 'x', 'R'), # Same for this one

    # For all of the below, transitions to the reject state are omitted
    ('q2', '#'): ('q4', '#', 'R'),
    ('q2', '0'): ('q2', '0', 'R'),
    ('q2', '1'): ('q2', '1', 'R'),

    ('q3', '#'): ('q5', '#', 'R'),
    ('q3', '0'): ('q3', '0', 'R'),
    ('q3', '1'): ('q3', '1', 'R'),

    ('q4', '0'): ('q6', 'x', 'L'),
    ('q4', 'x'): ('q4', 'x', 'R'),

    ('q5', '1'): ('q6', 'x', 'L'),
    ('q5', 'x'): ('q5', 'x', 'R'),

    ('q6', '#'): ('q7', '#', 'L'),
    ('q6', '0'): ('q6', '0', 'L'),
    ('q6', '1'): ('q6', '1', 'L'),
    ('q6', 'x'): ('q6', 'x', 'L'),

    ('q7', '0'): ('q7', '0', 'L'),
    ('q7', '1'): ('q7', '1', 'L'),
    ('q7', 'x'): ('q1', 'x', 'R'),

    ('q8', '_'): ('qa', '_', 'R'),
    ('q8', 'x'): ('q8', '0', 'R'),
}
# Create TM itself
M1 = TM(tran1, 'q1', 'qa', 'qr', reserved_letters={'x', '_'}) # Blank '_' is special and doesn't strictly need to be listed as reserved, but it can be

print('\n' * 4)
print('#### TM M1 ####')
print(f'How M1 appears in text: {M1}')

print(f'M1 accepts "0#0": {M1.accepts('0#0')}')
print(f'M1 accepts "0110#0101": {M1.accepts('0110#0101')}')
print(f'M1 accepts "011010#011010": {M1.accepts('011010#011010')}')

print('Below is the language of M1 up to length 8:')
print(M1.L(8))

print('Below is the transition table of M1:')
M1.transition_table()




'''
Turing Machine M2 in Sipser, p172

M2 recognises the language {0^(2^n) | n >= 0}
'''
# Transition table
tran2 = {
    # NOTE transitions to the reject state can be omitted
    ('q1', '_'): ('qr', '_', 'R'),
    ('q1', 'x'): ('qr', 'x', 'R'),
    ('q1', '0'): ('q2', '_', 'R'),

    ('q2', '_'): ('qa', '_', 'R'),
    ('q2', 'x'): ('q2', 'x', 'R'),
    ('q2', '0'): ('q3', 'x', 'R'),

    ('q3', '_'): ('q5', '_', 'L'),
    ('q3', 'x'): ('q3', 'x', 'R'),
    ('q3', '0'): ('q4', '0', 'R'),

    ('q4', '_'): ('qr', '_', 'R'),
    ('q4', 'x'): ('q4', 'x', 'R'),
    ('q4', '0'): ('q3', 'x', 'R'),

    ('q5', '_'): ('q2', '_', 'R'),
    ('q5', 'x'): ('q5', 'x', 'L'),
    ('q5', '0'): ('q5', '0', 'L')
}
# Create TM itself
M2 = TM(tran2, 'q1', 'qa', 'qr', {'x'}) # No '_' needed and no keyword needed for reserved letters

print('\n' * 4)
print('#### TM M2 ####')
print(f'How M2 appears in text: {M2}')

print(f'M2 accepts "0": {M2.accepts('0')}')
print(f'M2 accepts "000": {M2.accepts('000')}')
print(f'M2 accepts "00000000": {M2.accepts('00000000')}')

print('Below is the language of M2 up to length 64:')
print(M2.L(64))

print('Below is the transition table of M2:')
M2.transition_table()