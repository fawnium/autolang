from autolang.backend.utils import words_to_length
from autolang.backend.machines.structs_transition import TransitionDFA
from autolang.backend.machines.settings_machines import DEFAULT_LANGUAGE_LENGTH

from autolang.visuals.dfa_visuals import _transition_table_dfa, _get_dfa_digraph
from autolang.visuals.render_diagrams import render_digraph
from autolang.visuals.display_diagrams import display_figure

from collections.abc import Iterable, Generator

class DFA:

    def __init__(self, 
                 transition: dict[tuple[str, str], str], 
                 start: str, 
                 accept: Iterable[str]):
        
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
    
    def accepts(self, 
                word: str) -> bool:
        
        if not isinstance(word, str): raise TypeError(f'Input word \'{word}\' is not a string.')
        if not all(letter in self.alphabet for letter in word): # Auto-reject if any unrecognised letters. TODO maybe this should raise an error instead?
            return False
        current = self.start # Initialise
        for letter in word: # Main compute loop
            current = self.transition[(current, letter)] # Transition to next state
        return current in self.accept # True if current state is in accept after word has been read
    
    # Generate language of DFA up to given length
    # By default, returns tuple up-front, returns generator if lazy = True
    def L(self, 
          n: int = DEFAULT_LANGUAGE_LENGTH, 
          lazy: bool = False) -> tuple[str, ...] | Generator[str]:
        
        # Generator object that produces words accepted by DFA
        gen = (word for word in words_to_length(n, self.alphabet) if self.accepts(word))
        return gen if lazy else tuple(gen)

    # VISUALISATION METHODS

    # Print transition table
    def transition_table(self):
        print(f'Transition table of {repr(self)}:')
        _transition_table_dfa(self.transition)

    # Create transition diagram of DFA
    # Either plots directly or saves
    def transition_diagram(self, *,
                           mode: str | None = None,
                           filename: str | None = None,
                           layout: str | None = None):
        '''
        - `mode`: either 'save' or 'show'
            - auto-detected if None
        - `filename`: name of saved image file if 'save' mode
        - `layout`: nx layout algorithm used for plotting, e.g. 'shell'
        '''
        # Create nx digraph encoding DFA
        digraph = _get_dfa_digraph(self.transition, self.start, self.accept)
        # Create matplotlib figure that plots digraph
        fig = render_digraph(digraph, layout)
        # Show/save final diagram
        display_figure(fig, mode, filename)

