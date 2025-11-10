class ConfigNFA:
    '''
    - `Config` object is a node in the computation tree of NFA
    - identified by the current `state` and remaing `suffix` of word being read, including letter being read by current state
    - also stores computation history `path` as a sequence of (state, letter) pairs, staring with (start_state, initial_letter)
    - NOTE path 'lags behind' other data by one computation step, since path records what has already happened, not what needs to happen next
    '''
    def __init__(self, state: str, suffix: str, path: tuple[tuple[str, str]] = tuple()):
        self.state = state
        self.suffix = suffix
        self.path = path

    def __repr__(self):
        path_str = ''.join([f'({state}, {letter})->' for state, letter in self.path])[:-2] if self.path else '' 
        return f'ConfigNFA(state: {self.state}, suffix: {self.suffix}, path: {path_str or ''})'
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        if not isinstance(other, ConfigNFA):
            return NotImplemented
        return (self.state == other.state) and (self.suffix == other.suffix)
    
    def __hash__(self):
        return hash((self.state, self.suffix))
    

class ConfigPDA:
    '''
    - `Config` object is a node in the computation tree of PDA
    - identified by the current `state`, remaing `suffix` of word being read (incl. current letter), and current `stack`
    - also stores computation history `path` as a sequence of (state, letter, stack) tuples, staring with (start_state, initial_letter, '')
    - NOTE path 'lags behind' other data by one computation step, since path records what has already happened, not what needs to happen next
    '''
    def __init__(self, state: str, suffix: str, stack: str = '', path: tuple[tuple[str, str, str]] = tuple()):
        self.state = state
        self.suffix = suffix
        self.stack = stack
        self.path = path

    def __repr__(self):
        path_str = ''.join([f'({state}, {letter}, {stack})->' for state, letter, stack in self.path])[:-2] if self.path else ''
        return f'ConfigPDA(state: {self.state}, suffix: {self.suffix}, stack: {self.stack}, path: {path_str or ''})'
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        if not isinstance(other, ConfigPDA):
            return NotImplemented
        return (self.state == other.state) and (self.suffix == other.suffix) and (self.stack == other.stack)
    def __hash__(self):
        return hash((self.state, self.suffix, self.stack))


class ConfigTM:
    '''
    TM config tracks the tape, current state, current head position, and transition history for logging, for each step in the computation.
    '''

    def __init__(self, 
                 state: str, 
                 tape: list[str], 
                 head: int, 
                 path: tuple[tuple[str, str]] = tuple()):
        self.state = state # Current state
        self.tape = tape # Current tape
        self.head = max(head, 0) # Tape head position
        self.path = path

    def __repr__(self):
        config = ''.join(self.tape[:self.head]) # Tape before head position
        config += '(' + self.state + ')' # Current state, encoding head position
        config += ''.join(self.tape[self.head:]) # Tape after head, including head position itself
        if config.endswith(')'): config += '_' # Add blank cell if head is at end of tape, to reduce ambiguity
        return config
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, other):
        if not isinstance(other, ConfigTM):
            return NotImplemented
        return (self.state == other.state) and (self.tape == other.tape) and (self.head == other.head)
    def __hash__(self):
        return hash((self.state, tuple(self.tape), self.head))

