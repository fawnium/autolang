from autolang.backend.utils import words_to_length
from autolang.backend.machines.structs_config import ConfigTM
from autolang.backend.machines.structs_transition import TransitionTM
from autolang.backend.machines.settings_machines import (DEFAULT_LANGUAGE_LENGTH,
                                                         DEFAULT_TM_ACCEPT, 
                                                         DEFAULT_TM_REJECT, 
                                                         DEFAULT_TM_BLANK, 
                                                         DEFAULT_TM_LEFT, 
                                                         DEFAULT_TM_RIGHT,
                                                         DEFAULT_TM_MAX_STEPS)

from autolang.visuals.tm_visuals import _transition_table_tm, _get_tm_digraph
from autolang.visuals.render_diagrams import render_digraph
from autolang.visuals.display_diagrams import display_figure

from collections.abc import Iterable, Generator


class TM:

    # NOTE the TM model used assumes single unique accept *and* reject states, and number of total states excludes these by choice
    # NOTE model also uses singly-infinite tape *not* doubly-infinite, so no left side before start cell
    # `reserved_letters` arg is for letters which are only for the tape alphabet and NOT the input alphabet

    def __init__(self, 
                 transition: dict[tuple[str, str], tuple[str, str, str]], 
                 start: str, 
                 accept: str = DEFAULT_TM_ACCEPT, 
                 reject: str = DEFAULT_TM_REJECT, 
                 reserved_letters: Iterable[str] = set()):
        
        self.transition = TransitionTM(transition, accept, reject, reserved_letters) # Wrap transition function and check valid encoding, and ensure halting states are valid
        self.states = self.transition.states
        self.input_alphabet = self.transition.input_alphabet
        self.tape_alphabet = self.transition.tape_alphabet
        self.accept = accept
        self.reject = reject
        # Check start state is valid
        if start not in self.states:
            raise ValueError(f'TM start state \'{start}\' must be included in list of states.')
        self.start = start
        self.MAX_STEPS = DEFAULT_TM_MAX_STEPS # Compute-step limit to catch undetected infinite loops

    # Represent TM in text
    def __repr__(self):
        return f'<{len(self.states) - 2}-state TM with input alphabet {'{' + ','.join(self.input_alphabet) + '}'} and tape alphabet {'{' + ','.join(self.tape_alphabet) + '}'}>'
    def __str__(self):
        return self.__repr__()
    
    # Move tape head and dynamically resize tape list if needed
    def move(self, 
             head: int, 
             tape: list[str], 
             direction: str) -> tuple[int, list[str]]:
        
        direction = direction.upper()
        if direction == DEFAULT_TM_LEFT:
            head = max(head - 1, 0) # Prevent moving past start cell
        elif direction == DEFAULT_TM_RIGHT:
            head += 1
            if head >= len(tape): # Pad tape if exploring new cells
                tape += [DEFAULT_TM_BLANK] * (head - len(tape) + 1)
        else:
            raise ValueError(f'Unrecognised direction \'{direction}\' for TM.')
        return head, tape
    
    # Transition to next config by reading current letter
    def next_config(self, 
                    config: ConfigTM) -> ConfigTM:
        
        # Extract current config
        state = config.state
        tape = config.tape
        head = config.head
        letter = tape[head] if tape else DEFAULT_TM_BLANK
        # Update machine
        next_state, next_letter, direction = self.transition[(state, letter)]
        tape[head] = next_letter # Write current cell
        head, tape = self.move(head, tape, direction) # Update tape head
        next_path = config.path + ((state, letter),) if config.path else ((state, letter),) # Update path by appending most recent transition
        return ConfigTM(next_state, tape, head, next_path)
    
    # Compute input word and decide acceptance
    def accepts(self, 
                word: str) -> bool: # Returns `None` if input word undecidable
        '''
        - Transition through configs until accept/reject state reached, or total steps exceeds limit `MAX_STEPS`
        - Only one config variable `current` needed (no `queue`) due to determinism
        - return: True = accept, False = reject, None = undecided (either likely undecidable or definitely undecidable)
        '''
        # Check input
        if DEFAULT_TM_BLANK in word:
            raise ValueError(f'Letter \'{DEFAULT_TM_BLANK}\' is reserved for tape use and cannot be used as input.')
        if not all(letter in self.input_alphabet for letter in word): # Reject if unrecognised symbols in input, TODO maybe raise error instead?
            return False

        tape = [letter for letter in word] if word else [DEFAULT_TM_BLANK] # Initialise tape
        current = ConfigTM(self.start, tape, 0, None) # Current config, including state and tape data - initialise as start
        steps = 0 # Number of steps executed
        visited = set() # Track seen configs to detect infinite loops
        visited.add(current)
        # Run until machine enters halting state, or `steps` overflows
        halting = {self.accept, self.reject}
        while (current.state not in halting) and (steps < self.MAX_STEPS):
            current = self.next_config(current)
            steps += 1
            if current in visited:
                return None # Abort if circular computation, since word can't be decided
            visited.add(current)
        # Decide accept/reject/undecided
        if current.state == self.accept:
            return True
        elif current.state == self.reject:
            return False
        else:
            return None # Case where max steps exceeded
        
    # Generate language of TM up to given length
    # By default, returns tuple up-front, returns generator if lazy = True
    def L(self, 
          n: int = DEFAULT_LANGUAGE_LENGTH, 
          lazy: bool = False) -> tuple[str, ...] | Generator[str]:
        
        # Generator object that produces words accepted by TM
        gen = (word for word in words_to_length(n, self.input_alphabet) if self.accepts(word))
        return gen if lazy else tuple(gen)

    # VISUALISATION METHODS

    # Print transition table
    def transition_table(self):
        print(f'Transition table of {repr(self)}:')
        _transition_table_tm(self.transition)

    # Create transition diagram of TM
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
        digraph = _get_tm_digraph(self.transition, self.start, self.accept, self.reject, filename)
        # Create matplotlib figure that plots digraph
        fig = render_digraph(digraph, layout)
        # Show/save final diagram
        display_figure(fig, mode, filename, kind='TM')