from autolang.backend.utils import words_to_length
from autolang.backend.machines.structs_config import ConfigPDA
from autolang.backend.machines.structs_transition import TransitionPDA
from autolang.backend.machines.settings_machines import DEFAULT_LANGUAGE_LENGTH

from autolang.visuals.pda_visuals import _transition_table_pda, _get_pda_digraph
from autolang.visuals.render_diagrams import render_digraph
from autolang.visuals.display_diagrams import display_figure

from collections.abc import Iterable, Generator

class PDA:
    # NOTE stack is represented as a string *not* a list of chars, and the top is defined as the start (stack[0])

    def __init__(self, 
                 transition: dict[tuple[str, str, str], tuple[tuple[str, str], ...]], 
                 start: str, 
                 accept: Iterable[str]):
        
        self.transition = TransitionPDA(transition) # Wrap transition function and check valid encoding
        self.states = self.transition.states
        self.input_alphabet = self.transition.input_alphabet
        self.stack_alphabet = self.transition.stack_alphabet
        # Check additional args agree with `transition`
        if start not in self.states:
            raise ValueError(f'PDA start state \'{start}\' must be included in list of states.')
        for state in accept:
            if state not in self.states:
                raise ValueError(f'PDA accept state \'{state}\' is invalid as it is not listed in the transition function.')
        self.start = start
        self.accept = set(accept) # Convert to set for fast lookup (probably unnecessary)

    # Represent PDA in text
    def __repr__(self):
        return f'<{len(self.states)}-state PDA with input alphabet {'{' + ','.join(self.input_alphabet) + '}'} and stack {'{' + ','.join(self.stack_alphabet) + '}'}>'
    def __str__(self):
        return self.__repr__()
    
    # Get list of next configs reachable from current state, next letter, and stack top - including via not reading one or both of latter
    def next_configs(self, 
                     config: ConfigPDA) -> tuple[ConfigPDA]:
        
        configs = [] # All reachable next configs, filled below
        # Extract current config
        current_state = config.state
        current_suffix = config.suffix
        current_stack = config.stack
        current_letter = current_suffix[0] if current_suffix else ''
        current_stack_top = current_stack[0] if current_stack else ''
        # Try all four combinations of reading/not reading next letter and stack top
        for letter in set((current_letter, '')): # Avoid double compute in case that `current_letter` is empty (i.e. no input suffix left)
            for stack_top in set((current_stack_top, '')): # Same redundancy in case of empty stack
                key = (current_state, letter, stack_top)
                if key in self.transition:
                    # Add new config for each next state allowed by transition
                    for next_state, stack_push in self.transition[key]:
                        # Handle new config attributes differently depending on whether input/stack letters read or not read
                        next_suffix = current_suffix[1:] if letter else current_suffix # Only consume next letter in input word if read letter is not ''
                        next_stack = stack_push + current_stack[1:] if stack_top else stack_push + current_stack # Only pop first letter from stack if stack read is not ''
                        next_path = config.path + ((current_state, letter, current_stack),) # Update path
                        configs.append(ConfigPDA(next_state, next_suffix, next_stack, next_path))
        return configs
    
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
        if not all(letter in self.input_alphabet for letter in word): # Reject if unrecognised symbols in input # TODO maybe raise error instead of auto-reject?
            return False
        
        queue = [ConfigPDA(self.start, word, '', tuple())] # Initialise list of configs to explore
        visited = set() # Track seen configs to prevent redunant branches and infinite loops

        while queue:
            current = queue.pop(0)
            # Check for termination on accept
            if current.suffix == '' and current.state in self.accept:
                return True
            if current in visited:
                continue # Abort current branch if already explored
            visited.add(current)
            # If above checks passed, proceeed by transitioning to next branches
            queue += list(self.next_configs(current))
        return False
    
    # Generate language of PDA up to given length
    # By default, returns tuple up-front, returns generator if lazy = True
    def L(self, 
          n: int = DEFAULT_LANGUAGE_LENGTH, 
          lazy: bool = False) -> tuple[str, ...] | Generator[str]:
        
        # Generator object that produces words accepted by PDA
        gen = (word for word in words_to_length(n, self.input_alphabet) if self.accepts(word))
        return gen if lazy else tuple(gen)

    # VISUALISATION METHODS

    # Print transition table
    def transition_table(self,
                         output: bool = True) -> str:
        '''
        - `output`: flag for printing directly to the terminal
        '''
        table = _transition_table_pda(self.transition)
        if output:
            print(f'Transition table of {repr(self)}:')
            print(table)
        return table
        
    # Create transition diagram of PDA
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
        # Create nx digraph encoding PDA
        digraph = _get_pda_digraph(self.transition, self.start, self.accept, filename)
        # Create matplotlib figure that plots digraph
        fig = render_digraph(digraph, layout)
        # Show/save final diagram
        display_figure(fig, mode, filename, kind='PDA')