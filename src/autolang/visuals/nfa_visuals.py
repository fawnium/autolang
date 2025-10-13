from autolang.backend.machines.structs_transition import TransitionNFA
from autolang.visuals.magic_chars import V, H, UL, UR, DL, DR, UDL, UDR, ULR, DLR, UDLR, EPSILON, EMPTY
from autolang.visuals.settings_visuals import DEFAULT_ACCEPT_COL, DEFAULT_REJECT_COL
from autolang.visuals.utils_visuals import get_edge_label

from collections.abc import Iterable

import networkx as nx

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


def _get_nfa_digraph(transition: TransitionNFA, start: str, accept: Iterable[str]) -> nx.DiGraph:

    # Helper to determine node colour
    def get_node_col(state: str, accept_col: str = DEFAULT_ACCEPT_COL, reject_col: str = DEFAULT_REJECT_COL) -> str:
        return accept_col if state in accept else reject_col

    # Map (state, next_state) edges to respective label
    # Collect letters together for edges between the same states
    edge_label_map = {}
    for (state, letter), next_states in transition.items():
        for next_state in next_states:
            if (state, next_state) in edge_label_map:
                edge_label_map[(state, next_state)].append(letter)
            else:
                edge_label_map[(state, next_state)] = [letter]
    # Convert labels from lists of letters to formatted strings
    edge_label_map = {(state, next_state): get_edge_label(letters) for (state, next_state), letters in edge_label_map.items()}

    # Create final digraph
    digraph = nx.DiGraph()
    # Add nodes
    for state in transition.states:
        digraph.add_node(state, color = get_node_col(state))
    # Add edges
    for (state, next_state), label in edge_label_map.items():
        digraph.add_edge(state, next_state, label = label)
    # Add metadata
    digraph.graph['start'] = start
    digraph.graph['accept'] = tuple(accept)
    digraph.graph['name'] = 'NFA with ' + str(len(transition.states)) + ' states and alphabet {' + ','.join(transition.alphabet) + '}'
    return digraph

