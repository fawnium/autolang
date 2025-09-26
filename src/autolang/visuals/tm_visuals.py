from autolang.backend.machines.structs_transition import TransitionTM, DEFAULT_BLANK, DEFAULT_LEFT, DEFAULT_RIGHT
from autolang.visuals.magic_chars import V, H, UL, UR, DL, DR, UDL, UDR, ULR, DLR, UDLR, EPSILON, EMPTY

# Helper to format table entries
def next_config_to_str(config: tuple[str, str, str], halting: tuple[str, str]) -> str:
    # Case for entering halting state - no need for write or direction
    if config[0] in halting: return config[0]
    # Normal case
    return '(' + config[0] + ',' + config[1] + ',' + config[2] + ')'


# Print formatted transition table of TM
# NOTE this function is only called by `TM` object
# NOTE all args are assumed valid and no input handling occurs here
def _transition_table_tm(transition: TransitionTM):
    # Unpack states and alphabet
    states = transition.states
    tape_alphabet = transition.tape_alphabet
    halting = (transition.accept, transition.reject)
    # Find widest table entry and number of non-header columns
    width = max([len(next_config_to_str(config, halting)) for config in transition.values()]) # Max width of cell in table for setting col width
    num = len(tape_alphabet) # Number of non-header cols
    # Helper to pad cells with whitespace
    def cell(s: str) -> str:
        return s + (' ' * (width - len(s)))
    # Print top border and header line of letters
    def print_header():
        print(DR + (H * width) + (num * (DLR + (H * width))) + DL)
        print(V + (width * ' ') + V + V.join(cell(letter) for letter in tape_alphabet) + V)
    # Print bottom border
    def print_footer():
        print(UR + (H * width) + (num * (ULR + (H * width))) + UL)
    # Print row of entries in table
    def print_line(state: str):
        line = V + cell(state) # State header cell
        for letter in tape_alphabet: # Add value cells
            next_config = transition.get((state, letter))
            line += V + cell(next_config_to_str(next_config, halting))
        line += V
        print(line)
    # Print line between table rows
    def print_filler_line(): 
        print(UDR + (H * width) + (num * (UDLR + (H * width))) + UDL)
    # Print formatted transition table
    print_header()
    for state in (state for state in states if state not in halting): # Omit rows for halting states
        print_filler_line()
        print_line(state)
    print_footer()