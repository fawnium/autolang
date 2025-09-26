from autolang.backend.utils import words_to_length
from autolang.backend.machines.structs_transition import TransitionDFA
from autolang.visuals.dfa_visuals import _transition_table_dfa
from collections.abc import Iterable

class DFA:

    def __init__(self, transition: dict[tuple[str, str], str], start: str, accept: Iterable[str]):
        self.transition = TransitionDFA(transition) # Wrap transition function and check valid encoding
        self.states = self.transition.states # Unpack states
        self.alphabet = self.transition.alphabet # Unpack alphabet
        # Check additional args agree with `transition`
        if start not in self.states:
            raise ValueError(f'DFA start state \'{start}\' must be included in list of states.')
        for state in accept:
            if state not in self.states:
                raise ValueError(f'DFA accept state \'{state}\' is invalid as it is not listed in the transition function.')
        self.start = start
        self.accept = set(accept)
        
    # Represent DFA in text
    def __repr__ (self):
        return f'<{len(self.states)}-state DFA with alphabet {'{' + ','.join(self.alphabet) + '}'}>'
    def __str__(self):
        return self.__repr__()
    
    def accepts(self, word: str) -> bool:
        if not isinstance(word, str): raise TypeError(f'Input word \'{word}\' is not a string.')
        if not all(letter in self.alphabet for letter in word): # Auto-reject if any unrecognised letters. TODO maybe this should raise an error instead?
            return False
        current = self.start # Initialise
        for letter in word: # Main compute loop
            current = self.transition[(current, letter)] # Transition to next state
        return current in self.accept # True if current state is in accept after word has been read
    
    # Generate language of DFA up to given length
    def L(self, n: int = 5) -> tuple[str, ...]:
        return tuple(word for word in words_to_length(n, self.alphabet) if self.accepts(word))

    # VISUALISATION METHODS

    # Print transition table
    def transition_table(self):
        print(f'Transition table of {repr(self)}:')
        _transition_table_dfa(self.transition)

    # Transition diagram (WIP v0.2.0)
    def transition_diagram(self):
        raise NotImplementedError
