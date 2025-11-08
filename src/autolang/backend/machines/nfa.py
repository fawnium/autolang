from autolang.backend.utils import words_to_length
from autolang.backend.machines.structs_config import ConfigNFA
from autolang.backend.machines.structs_transition import TransitionNFA
from autolang.backend.machines.settings_machines import DEFAULT_LANGUAGE_LENGTH

from autolang.visuals.nfa_visuals import _transition_table_nfa, _get_nfa_digraph
from autolang.visuals.render_diagrams import render_digraph
from autolang.visuals.display_diagrams import display_figure

from collections.abc import Iterable, Generator

class NFA:

    def __init__(self, 
                 transition: dict[tuple[str, str], tuple[str, ...]], 
                 start: str, 
                 accept: Iterable[str]):
        
        self.transition = TransitionNFA(transition) # Wrap transition function and check valid encoding
        self.states = self.transition.states
        self.alphabet = self.transition.alphabet
        # Check additional args agree with `transition`
        if start not in self.states:
            raise ValueError(f'NFA start state \'{start}\' must be included in list of states.')
        for state in accept:
            if state not in self.states:
                raise ValueError(f'NFA accept state \'{state}\' is invalid as it is not listed in the transition function.')
        self.start = start
        self.accept = set(accept)

    # Represent NFA in text
    def __repr__(self):
        return f'<{len(self.states)}-state NFA with alphabet {'{' + ','.join(self.alphabet) + '}'}>'
    def __str__(self):
        return self.__repr__()
    
    # TODO refactor more into `next_states` from `accepts` as with PDA case?
    def next_states(self, 
                    state: str, 
                    letter: str) -> tuple[str, ...]:
        
        if state not in self.states:
            raise ValueError(f'State \'{state}\' is not a valid state for {self}.')
        if (letter not in self.alphabet) and (letter != ''):
            raise ValueError(f'Letter \'{letter}\' is not in the alphabet of {self}.')
        if (state, letter) not in self.transition:
            return tuple() # Empty next states if key not present, because no transitions
        return self.transition[(state, letter)]
    
    def accepts(self, 
                word: str) -> bool:
        '''
        - initialise `queue` with start state and whole input word
        - simulate all computation branches using BFS:
            - choose next branch from `queue`, and pop it
            - for each transition (incl. epsilon-) from the current state in this branch, add the corresponding new config to `queue`
                - NOTE: always choosing from the start of `queue` and adding to the end will ensure BFS implicitly
            - if no transitions, end the branch by not adding any new configs. This will happen automatically
            - if no remaining letters in `suffix`, and current state is an accept state, then break the loop and accept
        - if all branches end, either by having no valid transitions or if (all branches have empty `suffix` and no novel branches), then reject
        '''
        if not all(letter in self.alphabet for letter in word): # Reject if unrecognised symbols in input
            return False
        
        queue = [ConfigNFA(self.start, word)] # Initialise list of configs to explore
        visited = set() # Track seen configs to prevent redunant branches and infinite loops

        while queue:
            current = queue.pop(0)
            # Check for termination on accept
            if current.suffix == '' and current.state in self.accept:
                return True
            if current in visited:
                continue # Abort current branch if already explored
            visited.add(current)

            # Next letter-transitions
            state = current.state
            letter = current.suffix[0] if current.suffix else ''
            if current.suffix:
                for next_state in self.next_states(state, letter):
                    queue.append(ConfigNFA(next_state, current.suffix[1:], current.path + (state, letter)))

            # Next ε-transitions
            for next_state in self.next_states(state, ''):
                queue.append(ConfigNFA(next_state, current.suffix, current.path + (state, '')))
        return False
    
    # Generate language of NFA up to given length
    # By default, returns tuple up-front, returns generator if lazy = True
    def L(self, 
          n: int = DEFAULT_LANGUAGE_LENGTH, 
          lazy: bool = False) -> tuple[str, ...] | Generator[str]:
        
        # Generator object that produces words accepted by NFA
        gen = (word for word in words_to_length(n, self.alphabet) if self.accepts(word))
        return gen if lazy else tuple(gen)

    # VISUALISATION METHODS

    # Print transition table
    def transition_table(self):
        print(f'Transition table of {repr(self)}:')
        _transition_table_nfa(self.transition)

    # Create transition diagram of NFA
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
        digraph = _get_nfa_digraph(self.transition, self.start, self.accept, filename)
        # Create matplotlib figure that plots digraph
        fig = render_digraph(digraph, layout)
        # Show/save final diagram
        display_figure(fig, mode, filename, kind='NFA')
        