from autolang.backend.machines.structs_transition import TransitionDFA
from autolang.visuals.magic_chars import V, H, UL, UR, DL, DR, UDL, UDR, ULR, DLR, UDLR

# Print formatted transition table of DFA
# NOTE this function is only called by `DFA` object
# NOTE all args are assumed valid and no input handling occurs here
def _transition_table_dfa(transition: TransitionDFA):
    # Unpack states and alphabet
    states = transition.states
    alphabet = transition.alphabet
    # Find widest table entry and number of non-header columns
    width = max(len(state) for state in states) # Longest name of state for setting column width
    num = len(alphabet)
    # Helper to pad cells with whitespace
    def cell(s: str) -> str:
        return s + (' ' * (width - len(s)))
    # Print top border and header line of letters
    def print_header():
        print(DR + (H * width) + (num * (DLR + (H * width))) + DL)
        print(V + (width * ' ') + V + V.join(cell(letter) for letter in alphabet) + V)
    # Print bottom border
    def print_footer():
        print(UR + (H * width) + (num * (ULR + (H * width))) + UL)
    # Print row of entries in table
    def print_line(state: str):
        line = V + cell(state) # State header cell
        for letter in alphabet: # Add value cells
            next_state = transition.get((state, letter))
            line += V + cell(next_state)
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
    
