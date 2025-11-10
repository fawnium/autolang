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

# Generate string for formatted transition table of NFA
# NOTE this function is only called by `NFA` object
# NOTE all args are assumed valid and no input handling occurs here
def _transition_table_nfa(transition: TransitionNFA) -> str:
    # Unpack states and alphabet
    states = transition.states
    alphabet = transition.alphabet

    # Find widest table entry and number of non-header columns
    width = max(len(next_states_to_str(next_states)) for next_states in transition.values()) # Longest name of table entry for setting column width
    num = len(alphabet) + 1 # Number of non-header cols - must add 1 for epsilon col

    # Helper to pad cells with whitespace
    def cell(s: str) -> str:
        return s + (' ' * (width - len(s)))
    
    # Generate top border and header line of letters
    def header() -> str:
        top_border_line = DR + (H * width) + (num * (DLR + (H * width))) + DL
        header_line = V + (width * ' ') + V + V.join(cell(letter) for letter in alphabet) + V + cell(EPSILON) + V
        return top_border_line + '\n' + header_line + '\n'

    # Generate bottom border
    def footer() -> str:
        footer_line = UR + (H * width) + (num * (ULR + (H * width))) + UL
        return footer_line + '\n'

    # Generate row of entries in table
    def line(state: str) -> str:
        line = V + cell(state) # State header cell
        for letter in (alphabet + ('',)): # Add value cells incl. epsilon col
            next_states = transition.get((state, letter))
            line += V + cell(next_states_to_str(next_states))
        line += V
        return line + '\n'

    # Print line between table rows
    def filler_line() -> str: 
        filler_line = UDR + (H * width) + (num * (UDLR + (H * width))) + UDL
        return filler_line + '\n'

    # Generate complete formatted transition table
    table = ''
    table += header()
    for state in states:
        table += filler_line() + line(state)
    table += footer()
    return table


def _get_nfa_digraph(transition: TransitionNFA, 
                     start: str, 
                     accept: Iterable[str],
                     filename: str | None = None) -> nx.DiGraph:
    '''
    - `transition`: transition object for NFA
    - `start`: start state of NFA, NOTE must be included in `transition` states (not checked)
    - `accept`: collection of NFA accept states, NOTE must all be included in `transition` states (not checked)
    - `filename` (optional): name to be used to save image later if specified
    '''

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
    digraph.graph['title'] = 'NFA with ' + str(len(transition.states)) + ' states and alphabet {' + ','.join(transition.alphabet) + '}'
    digraph.graph['kind'] = 'NFA'
    digraph.graph['filename'] = filename
    return digraph

