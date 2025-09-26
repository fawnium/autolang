from autolang.backend.machines.structs_transition import TransitionNFA
from autolang.visuals.magic_chars import V, H, UL, UR, DL, DR, UDL, UDR, ULR, DLR, UDLR, EPSILON, EMPTY

# Helper to format list of next states as a table entry
def next_states_to_str(states: tuple[str, ...]) -> str:
    if not states: return EMPTY # Case where no next states
    return '{' + ','.join(sorted(states, key=lambda s: (len(s), s))) + '}' # Case where more than zero next states

# Print formatted transition table of NFA
# NOTE this function is only called by `NFA` object
# NOTE all args are assumed valid and no input handling occurs here
def _transition_table_nfa(transition: TransitionNFA):
    # Unpack states and alphabet
    states = transition.states
    alphabet = transition.alphabet
    # Find widest table entry and number of non-header columns
    width = max(len(next_states_to_str(next_states)) for next_states in transition.values()) # Longest name of table entry for setting column width
    num = len(alphabet) + 1 # Number of non-header cols - must add 1 for epsilon col
    # Helper to pad cells with whitespace
    def cell(s: str) -> str:
        return s + (' ' * (width - len(s)))
    # Print top border and header line of letters
    def print_header():
        print(DR + (H * width) + (num * (DLR + (H * width))) + DL)
        print(V + (width * ' ') + V + V.join(cell(letter) for letter in alphabet) + V + cell(EPSILON) + V)
    # Print bottom border
    def print_footer():
        print(UR + (H * width) + (num * (ULR + (H * width))) + UL)
    # Print row of entries in table
    def print_line(state: str):
        line = V + cell(state) # State header cell
        for letter in (alphabet + ('',)): # Add value cells incl. epsilon col
            next_states = transition.get((state, letter))
            line += V + cell(next_states_to_str(next_states))
        line += V
        print(line)
    # Print line between table rows
    def print_filler_line(): 
        print(UDR + (H * width) + (num * (UDLR + (H * width))) + UDL)
    # Print formatted transition table
    print_header()
    for state in states:
        print_filler_line()
        print_line(state)
    print_footer()
