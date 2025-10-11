from autolang.backend.utils import words_to_length
from autolang.backend.machines.structs_config import ConfigTM
from autolang.backend.machines.structs_transition import TransitionTM
from autolang.backend.machines.structs_transition import DEFAULT_ACCEPT, DEFAULT_REJECT, DEFAULT_BLANK, DEFAULT_LEFT, DEFAULT_RIGHT
from autolang.visuals.tm_visuals import _transition_table_tm
from collections.abc import Iterable, Generator

# Arbitrary limit to computation steps in case of non-halting with no infinite loops detected
DEFAULT_MAX_STEPS = int(1e8) # Default 100 million

class TM:

    # NOTE the TM model used assumes single unique accept *and* reject states, and number of total states excludes these by choice
    # NOTE model also uses singly-infinite tape *not* doubly-infinite, so no left side before start cell
    # `reserved_letters` arg is for letters which are only for the tape alphabet and NOT the input alphabet

    def __init__(self, transition: dict[tuple[str, str], tuple[str, str, str]], 
                 start: str, accept: str = DEFAULT_ACCEPT, reject: str = DEFAULT_REJECT, reserved_letters: Iterable[str] = set()):
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
        self.MAX_STEPS = DEFAULT_MAX_STEPS # Compute-step limit to catch undetected infinite loops

    # Represent TM in text
    def __repr__(self):
        return f'<{len(self.states) - 2}-state TM with input alphabet {'{' + ','.join(self.input_alphabet) + '}'} and tape alphabet {'{' + ','.join(self.tape_alphabet) + '}'}>'
    def __str__(self):
        return self.__repr__()
    
    # Move tape head and dynamically resize tape list if needed
    def move(self, head: int, tape: list[str], direction: str) -> tuple[int, list[str]]:
        direction = direction.upper()
        if direction == DEFAULT_LEFT:
            head = max(head - 1, 0) # Prevent moving past start cell
        elif direction == DEFAULT_RIGHT:
            head += 1
            if head >= len(tape): # Pad tape if exploring new cells
                tape += [DEFAULT_BLANK] * (head - len(tape) + 1)
        else:
            raise ValueError(f'Unrecognised direction \'{direction}\' for TM.')
        return head, tape
    
    # Transition to next config by reading current letter
    def next_config(self, config: ConfigTM) -> ConfigTM:
        # Extract current config
        state = config.state
        tape = config.tape
        head = config.head
        letter = tape[head] if tape else DEFAULT_BLANK
        # Update machine
        next_state, next_letter, direction = self.transition[(state, letter)]
        tape[head] = next_letter # Write current cell
        head, tape = self.move(head, tape, direction) # Update tape head
        next_path = config.path + ((state, letter),) if config.path else ((state, letter),) # Update path by appending most recent transition
        return ConfigTM(next_state, tape, head, next_path)
    
    # Compute input word and decide acceptance
    def accepts(self, word: str) -> bool: # Returns `None` if input word undecidable
        '''
        - Transition through configs until accept/reject state reached, or total steps exceeds limit `MAX_STEPS`
        - Only one config variable `current` needed (no `queue`) due to determinism
        - return: True = accept, False = reject, None = undecided (either likely undecidable or definitely undecidable)
        '''
        # Check input
        if DEFAULT_BLANK in word:
            raise ValueError(f'Letter \'{DEFAULT_BLANK}\' is reserved for tape use and cannot be used as input.')
        if not all(letter in self.input_alphabet for letter in word): # Reject if unrecognised symbols in input, TODO maybe raise error instead?
            return False

        tape = [letter for letter in word] if word else [DEFAULT_BLANK] # Initialise tape
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
    def L(self, n: int = 5, lazy: bool = False) -> tuple[str, ...] | Generator[str]:
        # Generator object that produces words accepted by TM
        gen = (word for word in words_to_length(n, self.input_alphabet) if self.accepts(word))
        return gen if lazy else tuple(gen)

    # VISUALISATION METHODS

    # Print transition table
    def transition_table(self):
        print(f'Transition table of {repr(self)}:')
        _transition_table_tm(self.transition)

    # Transition diagram (WIP v0.2.0)
    def transition_diagram(self):
        raise NotImplementedError