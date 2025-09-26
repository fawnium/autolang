from autolang.backend.regex.regex_input import alphabet_of
from autolang.backend.regex.regex_eliminate import RegexParserEliminate
from autolang.backend.machines.nfa import NFA

class GNFA:

    '''
    GNFA is quite similar to NFA in terms of structure, but is not intended for computing input words.
    The GNFA edges are not represented by a `Transition`-type object, but instead simply 3-tuples encoding end states and label.
    Also, GNFA edges can be labelled by arbitrary strings, not just letters from the alphabet.
    Aside from that the structure is more or less the same as that of the NFA. 
    Instead of methods for computing input words, it has methods for iteratively eliminating compound edge-labels.
    '''

    def __init__(self, regex: str):
        self.regex = regex # NOTE regex is already preprocessed and assumed valid when passed here
        self.states = ['s0', 't'] # Only start and accept states initially
        self.alphabet = alphabet_of(regex)
        self.edges = [('s0', 't', regex)] # Encode edges as (first state, second state, label)
        self.start = 's0'
        self.accept = 't'

    # Helper for naming added states
    def new_state(self):
        index = len(self.states) - 1 # States will be s0, s1, s2, ..., t
        return 's' + str(index)

    # Eliminate a union by replacing one edge with two parallel edges with child regexes
    def eliminate_union(self, state1: str, state2: str, regex1: str, regex2: str, original_regex: str):
        for state in (state1, state2):
            if state not in self.states:
                raise ValueError(f'State \'{state}\' is not recognised.')
        if (state1, state2, original_regex) not in self.edges:
            raise ValueError(f'Edge \'{(state1, state2, original_regex)}\' is not in GNFA.')
        self.edges.remove((state1, state2, original_regex))
        self.edges.append((state1, state2, regex1))
        self.edges.append((state1, state2, regex2))
        return True

    # Eliminate a concat by juxtaposing a new state connected by child edges
    def eliminate_concat(self, state1: str, state2: str, regex1: str, regex2: str, original_regex: str):
        for state in (state1, state2):
            if state not in self.states:
                raise ValueError(f'State \'{state}\' is not recognised.')
        if (state1, state2, original_regex) not in self.edges:
            raise ValueError(f'Edge \'{(state1, state2, original_regex)}\' is not in GNFA.')
        self.edges.remove((state1, state2, original_regex))
        state3 = self.new_state()
        self.states.append(state3)
        self.edges.append((state1, state3, regex1))
        self.edges.append((state3, state2, regex2))
        return True

    # Eliminate a star by isolating with e-transitions and adding a loop with child regex
    def eliminate_star(self, state1:str, state2: str, regex1: str, original_regex: str):
        for state in (state1, state2):
            if state not in self.states:
                raise ValueError(f'State \'{state}\' is not recognised.')
        if (state1, state2, original_regex) not in self.edges:
            raise ValueError(f'Edge \'{(state1, state2, original_regex)}\' is not in GNFA.')
        self.edges.remove((state1, state2, original_regex))
        state3 = self.new_state()
        self.states.append(state3)
        self.edges.append((state1, state3, ''))
        self.edges.append((state3, state2, ''))
        self.edges.append((state3, state3, regex1))
        return True

    # Run elimination loop until all edges primitive
    def eliminate(self):
        all_primitive = False # If all edges are either letters or empty
        while not all_primitive:
            seen_operator = False # Track non-primitive edges for each individual edge list iteration
            for edge in self.edges:
                '''
                NOTE since `self.edges` is mutable, iterating and modifying at the same time is risky. But since the parent while loop will keep iterating until 
                all edges were primitive in the last pass, skipped/doubled edge checks should be caught in the next `for` loop anyway. Therefore there shouldn't be 
                problems, and the parent loop will still terminate only when all edges are primitive.
                '''
                state1, state2, regex = edge[0], edge[1], edge[2] # Unpack edge
                elim_type, regexes = RegexParserEliminate.parse(regex) # Call parser to decide elimination type
                if elim_type == 'union':
                    seen_operator = True # Flag that another for loop is needed after current one
                    regex1 = regexes[0]
                    regex2 = regexes[1]
                    self.eliminate_union(state1, state2, regex1, regex2, regex)
                elif elim_type == 'concat':
                    seen_operator = True # Flag that another for loop is needed after current one
                    regex1 = regexes[0]
                    regex2 = regexes[1]
                    self.eliminate_concat(state1, state2, regex1, regex2, regex)
                elif elim_type == 'star':
                    seen_operator = True # Flag that another for loop is needed after current one
                    regex1 = regexes[0]
                    self.eliminate_star(state1, state2, regex1, regex)
                elif elim_type == 'primitive':
                    # Leave primitive edge as it is
                    pass
                else:
                    raise ValueError(f'Failed to parse regex \'{regex}\'.') # If `RegexParserEliminate` couldn't recognise input string
            if not seen_operator: # If all edges primitive after most recent pass, exit parent while loop
                all_primitive = True
        return True

    def to_nfa(self) -> NFA:
        # Ensure elimination has happened - function is idempotent so no problem if already ran
        self.eliminate()
        # Add each transition from `edges` to transition function
        # NOTE next states is initially a list for mutability, then converted to tuple
        transition = {}
        for state1, state2, letter in self.edges:
            # Ensure no brackets in labels, in case not caught in elimination loop
            letter = RegexParserEliminate.trim_enclosing_brackets(letter) # '(a)' -> 'a'
            if (state1, letter) in transition:
                transition[(state1, letter)].append(state2)
            else:
                transition[(state1, letter)] = [state2]
        transition = {key: tuple(sorted(val)) for key, val in transition.items()} # Convert next_states to tuples
        return NFA(transition, self.start, self.accept) # Create and return NFA

