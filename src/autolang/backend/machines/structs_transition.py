from autolang.backend.machines.settings_machines import (DEFAULT_TM_ACCEPT,
                                                         DEFAULT_TM_REJECT,
                                                         DEFAULT_TM_BLANK,
                                                         DEFAULT_TM_LEFT,
                                                         DEFAULT_TM_RIGHT,
                                                         FORBIDDEN_CHARS)

from collections.abc import Iterable

'''
Wrapper classes for transition function dicts
- responsible for ensuring correct transition encoding before creating automaton object
    - e.g. in TransitionDFA, ensure all state-letter pairs have a defined next state
- also responsible for extracting the respective lists of states and alphabets for automata
    - originally these were passed separately, but since they can be uniquely deduced from transition dict values, this was pointless
- not responsible for actually simulating automata, that is handled in the respective file e.g. dfa.py
'''


# Helper to check forbidden chars
def check_forbidden(obj):
    if not obj: return True
    for c in obj:
        if c in FORBIDDEN_CHARS:
            raise ValueError(f'Forbidden character \'{c}\' used in string.')
    return True
# Helper to check if 'letters' are single characters
# TODO(?) support multiple-char letters in a later version, maybe
def check_single_char(letter: str):
    if letter == '': return True # Edge case
    if len(letter) != 1:
        raise ValueError(f'This version of autolang only supports single characters in alphabets, but \'{letter}\' is multiple.')
    return True



class TransitionDFA:
    '''
    `function` is a dict, where each entry has the form `(state, letter): next_state` where all three 
    are strings, and `letter` is expected to be a single char.
    '''
    def __init__(self, function: dict[tuple[str, str], str]):
        self.function = function
        self.validate_type() # Check types before extraction
        self.states, self.alphabet = self.extract()
        self.validate_fullness()

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.function)})'
    def __str__(self):
        return str(self.function)

    # Deduce states and letters from transition `function`
    # Assumes `function` has been checked for valid types
    def extract(self) -> tuple[tuple[str, ...], tuple[str, ...]]: # returns `states, alphabet`
        states = set()
        alphabet = set()
        for (state, letter), next_state in self.function.items():
            check_forbidden(state); check_forbidden(letter); check_forbidden(next_state) # Check for forbidden chars
            check_single_char(letter) # Check letter is only one char
            states.update({state, next_state}) # Add states
            alphabet.add(letter) # Add letter
        states = tuple(sorted(states, key=lambda s: (len(s), s))) # Sort states in len-lex order, just in case
        alphabet = tuple(sorted(alphabet))
        return states, alphabet

    # Check `function` is a dict and all entries have the correct type
    def validate_type(self):
        if not isinstance(self.function, dict):
            raise TypeError('DFA transition function must be a dict.')
        for key in self.function:
            if not isinstance(key, tuple):
                raise TypeError(f'DFA transition key \'{key}\' must be a tuple, not {type(key)}.')
            if len(key) != 2:
                raise TypeError(f'DFA transition key \'{key}\' must have length 2, not {len(key)}.')
            state, letter = key
            if not isinstance(state, str):
                raise TypeError(f'DFA state \'{state}\' must be a string, not {type(state)}.')
            if not isinstance(letter, str):
                raise TypeError(f'DFA letter \'{letter}\' must be a string, not {type(letter)}.')
        for next_state in self.function.values():
            if not isinstance(next_state, str):
                raise TypeError(f'DFA state \'{next_state}\' must be a string, not {type(next_state)}.')
        return True

    # Check a transition is defined for every possible state-letter pair - must be true for DFA
    # Assumes states, alphabet already defined
    def validate_fullness(self):
        for key in [(state, letter) for state in self.states for letter in self.alphabet]:
            if key not in self.function:
                raise ValueError(f'DFA transition function is missing key \'{key}\'.')
        return True

    '''
    Duck typing to retrieve values
    '''
    def __getitem__(self, key: tuple[str, str]): # Support indexing e.g. TransitionDFA[('q0', 'a')]
        return self.function[key]
    def get(self, key: tuple[str, str], default = None): # Support .get() method
        return self.function.get(key, default)
    def __contains__(self, key: tuple[str, str]): # Support containment e.g. if ('q0', 'a') in TransitionDFA
        return key in self.function
    def items(self):
        return self.function.items()
    def values(self):
        return self.function.values()


class TransitionNFA:
    '''
    `function` is a dict, where each entry has the form `(state, letter): next_states := (next_state1, next_state1, ...)`
    - each state and letter is a string, and letters expected to be length 1
    - next_states can be an empty tuple if no transitions exist
    - NOTE ε-transitions are simply encoded as an empty string, e.g. ('q0', '') instead of ('q0', 'a')
    '''
    def __init__(self, function: dict[tuple[str, str], tuple[str, ...]]):
        self.function = function
        self.validate_type() # Check types before extraction
        self.states, self.alphabet = self.extract()

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.function)})'
    def __str__(self):
        return str(self.function)

    # Deduce states and letters from transition `function`
    # Assumes `function` has been checked for valid types
    def extract(self) -> tuple[tuple[str, ...], tuple[str, ...]]: # returns `states, alphabet`
        states = set()
        alphabet = set()
        for (state, letter), next_states in self.function.items():
            check_forbidden(state); check_forbidden(letter) # Check for forbidden chars
            for next_state in next_states:
                check_forbidden(next_state)
            check_single_char(letter) # Check letter is a single char
            states.update({state} | set(next_states)) # Add states
            alphabet.add(letter)
        states = tuple(sorted(states, key=lambda s: (len(s), s))) # Sort states in len-lex order, just in case
        alphabet.discard('') # Empty string should not be in alphabet, but is a valid 'letter' in transition function
        alphabet = tuple(sorted(alphabet))
        return states, alphabet

    # Check `function` is a dict and all entries have the correct type
    def validate_type(self):
        if not isinstance(self.function, dict):
            raise TypeError('NFA transition function must be a dict.')
        for key in self.function:
            if not isinstance(key, tuple):
                raise TypeError(f'NFA transition key \'{key}\' must be a tuple, not {type(key)}.')
            if len(key) != 2:
                raise TypeError(f'NFA transition key \'{key}\' must have length 2, not {len(key)}.')
            state, letter = key
            if not isinstance(state, str):
                raise TypeError(f'NFA state \'{state}\' must be a string, not {type(state)}.')
            if not isinstance(letter, str):
                raise TypeError(f'NFA letter \'{letter}\' must be a string, not {type(letter)}.')
        for next_states in self.function.values():
            if not isinstance(next_states, tuple):
                raise TypeError(f'NFA next states must be a tuple for all keys, not {type(next_states)}.')
            for next_state in next_states:
                if not isinstance(next_state, str):
                    raise TypeError(f'NFA state \'{next_state}\' must be a string, not {type(next_state)}.')
        return True
    '''
    Duck typing to retrieve values
    '''
    def __getitem__(self, key: tuple[str, str]):
        return self.function[key]
    def get(self, key: tuple[str, str], default = tuple()):
        return self.function.get(key, default)
    def __contains__(self, key: tuple[str, str]):
        return key in self.function
    def items(self):
        return self.function.items()
    def values(self):
        return self.function.values()


class TransitionPDA:
    '''
    `function` is a dict, where each entry has the form `(state, letter, stack_top): next_configs := ((next_state1, stack_push1), ...)`
    - each state and letter is a string, and letters expected to be length 1
    - next_states can be an empty tuple if no transitions exist
    - NOTE ε-transitions are simply encoded as an empty string, e.g. ('q0', '', '$) instead of ('q0', 'a', '$'), and similar for stack letters
    - NOTE autolang's PDA model can only process a single stack letter in each step
    '''
    def __init__(self, function: dict[tuple[str, str, str], tuple[tuple[str, str], ...]]):
        self.function = function
        self.validate_type()
        self.states, self.input_alphabet, self.stack_alphabet = self.extract()

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.function)})'
    def __str__(self):
        return str(self.function)

    # Deduce states, input letters, and stack letters from transition `function`
    # Assumes `function` has been checked for valid types
    def extract(self) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]: # Returns `states, input_alphabet, stack_alphabet`
        states = set()
        input_alphabet = set()
        stack_alphabet = set()
        for (state, letter, stack_top), next_configs in self.function.items():
            # Check for forbidden chars and that all letters are single chars
            check_forbidden(state); check_forbidden(letter); check_forbidden(stack_top)
            check_single_char(letter); check_single_char(stack_top)
            for next_state, stack_push in next_configs:
                check_forbidden(next_state); check_forbidden(stack_push)
                check_single_char(stack_push)
            # Add states and letters
            states.add(state)
            input_alphabet.add(letter)
            stack_alphabet.add(stack_top)
            for (next_state, stack_push) in next_configs:
                states.add(next_state)
                stack_alphabet.add(stack_push)
        states = tuple(sorted(states, key=lambda s: (len(s), s))) # Sort states in len-lex order, just in case
        input_alphabet.discard('') # Empty string should not be in alphabet, but is a valid 'letter' in transition function
        input_alphabet = tuple(sorted(input_alphabet))
        stack_alphabet.discard('')
        stack_alphabet = tuple(sorted(stack_alphabet))
        return states, input_alphabet, stack_alphabet

    # Check `function` is a dict and all entries have the correct type
    def validate_type(self):
        if not isinstance(self.function, dict):
            raise TypeError('PDA transition function must be a dict.')
        for key in self.function:
            if not isinstance(key, tuple):
                raise TypeError(f'PDA transition key \'{key}\' must be a tuple, not {type(key)}.')
            if len(key) != 3:
                raise TypeError(f'PDA transition key \'{key}\' must have length 3, not {len(key)}.')
            state, letter, stack_top = key
            if not isinstance(state, str):
                raise TypeError(f'PDA state \'{state}\' must be a string, not {type(state)}.')
            if not isinstance(letter, str):
                raise TypeError(f'PDA letter \'{letter}\' must be a string, not {type(letter)}.')
            if not isinstance(stack_top, str):
                raise TypeError(f'PDA stack letter \'{letter}\' must be a string, not {type(letter)}.')
        for next_configs in self.function.values():
            if not isinstance(next_configs, tuple):
                raise TypeError(f'PDA next configs must be a tuple for all keys, not {type(next_configs)}')
            for next_config in next_configs:
                if not isinstance(next_config, tuple):
                    raise TypeError(f'PDA next configs must all be tuples, not {type(next_config)}.')
                if len(next_config) != 2:
                    raise TypeError(f'PDA next configs must all have length 2 (next state and stack push), not {len(next_config)}.')
                next_state, stack_push = next_config
                if not isinstance(next_state, str):
                    raise TypeError(f'PDA state \'{next_state}\' must be a string, not {type(next_state)}.')
                if not isinstance(stack_push, str):
                    raise TypeError(f'PDA letter \'{stack_push}\' must be a string, not {type(stack_push)}.')
        return True

    # Ensure `(state, '', ''): (state, '')` in transition for all states
    # NOTE Unused, as it is not necessary and doesn't change behaviour?
    def validate_loops(self):
        for state in self.states:
            if (state, '', '') not in self.function:
                raise ValueError(f'PDA transition function is missing the trivial transition \'({state}, \'\', \'\') -> ({state}, \'\')\'.')
            if (state, '') not in self.function[(state, '', '')]:
                raise ValueError(f'PDA transition function is missing the trivial transition \'({state}, \'\', \'\') -> ({state}, \'\')\'.')
        return True
    '''
    Duck typing to retrieve values
    '''
    def __getitem__(self, key: tuple[str, str, str]):
        return self.function[key]
    def get(self, key: tuple[str, str, str], default = tuple()):
        return self.function.get(key, default)
    def __contains__(self, key:tuple[str, str, str]):
        return key in self.function
    def items(self):
        return self.function.items()
    def values(self):
        return self.function.values()


class TransitionTM:

    # NOTE this TM model does *not* allow neutral moves
    # NOTE this TM model's tape is only singly-infinite, i.e. it cannot move left past the start cell
    # NOTE currently the empty letter '' is allowed to be written to a cell as a regular letter, since only '_' is reserved to indicate a blank cell
        # TODO perhaps there should be better handling of '' - certainly it shouldn't be allowed as an input letter?
    '''
    `function` is a dict, where each entry has the form `(state, letter): next_config := (next_state, write, direction)

    `reserved_letters` arg is for letters which are only for the tape alphabet and NOT the input alphabet
        NOTE this does not include the blank letter '_', which is always reserved and hence handled independently
    '''

    def __init__(self, function: dict[tuple[str, str], tuple[str, str, str]], 
                 accept: str = DEFAULT_TM_ACCEPT, reject: str = DEFAULT_TM_REJECT, reserved_letters: Iterable[str] = set()):
        # Check halting states are distinct from each other
        if accept == reject:
            raise ValueError(f'TM accept and reject states cannot be equal (both \'{accept}\').')
        # Check reserved letters is the correct type
        if not isinstance(reserved_letters, Iterable) or not all(isinstance(letter, str) for letter in reserved_letters):
            raise TypeError('TM reserved letters are not correctly formatted.')
        self.function = function
        self.reserved_letters = set(reserved_letters)
        self.accept = accept; self.reject = reject
        self.validate_type()
        self.states, self.input_alphabet, self.tape_alphabet = self.extract()
        self.validate_fullness() # If missing transitions, add them and send them all to reject state

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self.function)})'
    def __str__(self):
        return str(self.function)

    # Deduce states, input letters, and tape letters from transition `function`
    # Assumes `function` has been checked for valid types
    # NOTE extraction assumes that *every* letter apart from '_' is supposed to be in the input alphabet, which may not be intended
        # Currently no way of indicating what should be excluded from input alphabet
    # TODO improve this in next version so that input and tape alphabets are correctly separated
    def extract(self) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
        states = set()
        input_alphabet = set()
        tape_alphabet = set()
        seen_accept = False # Track whether reserved accept state was seen in transition function
        for (state, letter), (next_state, write, _) in self.function.items(): # NOTE direction is not needed for extraction - already checked in `validate_type()`
            # Check letters are single chars
            check_single_char(letter); check_single_char(write)
            # If halting state appears in a key raise error, because that transition cannot occur anyway so assume user error
            if state in (self.accept, self.reject):
                raise ValueError(f'Unexpected appearance of halting state \'{state}\' in TM transition key.')
            # If accept state appears in value, just record its presence and handle after loop
            if next_state == self.accept: seen_accept = True
            # Add states and letters
            states.update({state, next_state})
            input_alphabet.update({letter, write})
            tape_alphabet.update({letter, write})
        # Handle missing accept state from transition function
        if not seen_accept:
            proceed = input(f'TM has no transitions to accept state \'{self.accept}\', so cannot accept any words. Proceed anyway? (Y/n): ')
            if proceed != 'Y':
                raise ValueError(f'TM is missing transitions to the accept state \'{self.accept}\'.')
        # Finish preparing returns
        states.update({self.accept, self.reject}) # Include halting states in list of states, regardless of whether they are in transition function
        states = tuple(sorted(states, key=lambda s: (len(s), s))) # Sort states in len-lex order, just in case
        input_alphabet.discard(DEFAULT_TM_BLANK) # Reserved blank letter cannot be used in input alphabet
        input_alphabet -= self.reserved_letters # Remove reserved tape letters from the input alphabet
        input_alphabet = tuple(sorted(input_alphabet))
        # Ensure reserved char '_' *does* appear in tape alphabet
        if DEFAULT_TM_BLANK not in tape_alphabet: # Triggers if '_' was not seen in any transition entry
            raise ValueError(f'TM transition is missing transitions for blank letter \'{DEFAULT_TM_BLANK}\'.')
        tape_alphabet = tuple(sorted(tape_alphabet))
        return states, input_alphabet, tape_alphabet

    # Check `function` is a dict and all entries have the correct type
    def validate_type(self):
        if not isinstance(self.function, dict):
            raise TypeError('TM transition function must be a dict.')
        for key in self.function:
            if not isinstance(key, tuple):
                raise TypeError(f'TM transition key \'{key}\' must be a tuple, not {type(key)}.')
            if len(key) != 2:
                raise TypeError(f'TM transition key \'{key}\' must have length 2, not {len(key)}.')
            state, letter = key
            if not isinstance(state, str):
                raise TypeError(f'TM state \'{state}\' must be a string, not {type(state)}.')
            if not isinstance(letter, str):
                raise TypeError(f'TM letter \'{letter}\' must be a string, not {type(letter)}.')
        for next_config in self.function.values():
            if not isinstance(next_config, tuple):
                raise TypeError(f'TM next config \'{next_config}\' must be a tuple, not {type(next_config)}.')
            if len(next_config) != 3:
                raise TypeError(f'TM next config must have length 3 (next state, write, direction), not {len(next_config)}.')
            next_state, write, direction = next_config
            if not isinstance(next_state, str):
                raise TypeError(f'TM state \'{next_state}\' must be a string, not {type(next_state)}.')
            if not isinstance(write, str):
                raise TypeError(f'TM letter \'{letter}\' must be a string, not {type(letter)}.')
            if direction not in (DEFAULT_TM_LEFT, DEFAULT_TM_RIGHT):
                raise TypeError(f'Unrecognised TM direction \'{direction}\'.')
        return True

    # Assume missing transitions go to reject state, and add them
    def validate_fullness(self):
        for key in [(state, letter) for state in self.states for letter in self.tape_alphabet if state not in (self.accept, self.reject)]:
            if key not in self.function:
                self.function[key] = (self.reject, key[1], 'R') # Silently add reject transition, and write same letter already in cell
    '''
    Duck typing to retrieve values
    '''
    def __getitem__(self, key: tuple[str, str]):
        return self.function[key]
    def get(self, key: tuple[str, str], default = None):
        return self.function.get(key, default)
    def __contains__(self, key:tuple[str, str]):
        return key in self.function
    def items(self):
        return self.function.items()
    def values(self):
        return self.function.values()
