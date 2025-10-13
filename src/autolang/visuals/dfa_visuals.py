from autolang.backend.machines.structs_transition import TransitionDFA
from autolang.visuals.magic_chars import V, H, UL, UR, DL, DR, UDL, UDR, ULR, DLR, UDLR

import networkx as nx

from collections.abc import Iterable

# Maximum length of edge label before abbreviating
MAX_LABEL_LENGTH = 8

# Default colours for states in transition diagram
DEFAULT_ACCEPT_COL = 'lightgreen'
DEFAULT_REJECT_COL = 'white'
DEFAULT_START_ACCEPT_COL = 'green'
DEFAULT_START_REJECT_COL = 'gray'

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
    

def _get_dfa_digraph(transition: TransitionDFA, start: str, accept: Iterable[str]) -> nx.DiGraph:

    # Helper to generate edge labels
    def get_edge_label(letters: Iterable[str], max_length = MAX_LABEL_LENGTH) -> str:
        letters = sorted(letters)
        # Total length is sum of lengths of letters plus number of commas added
        length = sum(len(letter) for letter in letters) + (len(letters) - 1)
        # Join all letters by commas if total length short enough
        if length <= max_length:
            return ','.join(letters)
        # Only join some if total too long
        else:
            # TODO handle edge case where only one letter?
            # TODO not just start and end, but as many as possible while still under max length?
            return letters[0] + ',...,' + letters[-1]
        
    # Helper to determine node colour
    def get_node_col(state: str, accept_col: str = DEFAULT_ACCEPT_COL, reject_col: str = DEFAULT_REJECT_COL,
                     start_accept_col: str = DEFAULT_START_ACCEPT_COL, start_reject_col: str = DEFAULT_START_REJECT_COL):
        if state == start:
            return start_accept_col if state in accept else start_reject_col
        else:
            return accept_col if state in accept else reject_col
        
    # Map (state, next_state) edges to respective label
    # Collect letters together for edges between the same states
    edge_label_map = {}
    for (state, letter), next_state in transition.items():
        if (state, next_state) in edge_label_map:
            edge_label_map[(state, next_state)].append(letter)
        else:
            edge_label_map[(state, next_state)] = [letter]
    # Convert labels from lists of letters to formatted strings
    edge_label_map = {(state, next_state): get_edge_label(letters) for (state, next_state), letters in edge_label_map.items()}
        
    # Create final digraph
    G = nx.DiGraph()
    # Add nodes
    for state in transition.states:
        G.add_node(state, color = get_node_col(state))
    # Add edges
    for (state, next_state), label in edge_label_map.items():
        G.add_edge(state, next_state, label = label)
    # Add metadata in case needed later
    G.graph['start'] = start
    G.graph['accept'] = tuple(accept)
    return G
