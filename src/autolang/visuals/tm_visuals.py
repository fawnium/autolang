from autolang.backend.machines.structs_transition import TransitionTM
from autolang.visuals.magic_chars import V, H, UL, UR, DL, DR, UDL, UDR, ULR, DLR, UDLR, EPSILON, EMPTY
from autolang.visuals.settings_visuals import DEFAULT_ACCEPT_COL, DEFAULT_REJECT_COL
from autolang.visuals.utils_visuals import get_edge_label_tm

from collections.abc import Iterable

import networkx as nx

# Helper to format table entries
def next_config_to_str(config: tuple[str, str, str], halting: tuple[str, str]) -> str:
    '''
    - `config`: of the form (letter, write, direction)
    - `halting`: pair of accept and reject states, for formatting edge case
    '''
    # Case for entering halting state - no need for write or direction
    if config[0] in halting: return config[0]
    # Normal case
    return '(' + config[0] + ',' + config[1] + ',' + config[2] + ')'


# Generate string for formatted transition table of TM
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
    
    # Generate top border and header line of letters
    def header() -> str:
        top_border_line = DR + (H * width) + (num * (DLR + (H * width))) + DL
        header_line = V + (width * ' ') + V + V.join(cell(letter) for letter in tape_alphabet) + V
        return top_border_line + '\n' + header_line + '\n'

    # Generate bottom border
    def footer() -> str:
        footer_line = UR + (H * width) + (num * (ULR + (H * width))) + UL
        return footer_line + '\n'

    # Generate row of entries in table
    def line(state: str) -> str:
        line = V + cell(state) # State header cell
        for letter in tape_alphabet: # Add value cells
            next_config = transition.get((state, letter))
            line += V + cell(next_config_to_str(next_config, halting))
        line += V
        return line + '\n'

    # Generate line between table rows
    def filler_line() -> str: 
        filler_line = UDR + (H * width) + (num * (UDLR + (H * width))) + UDL
        return filler_line + '\n'

    # Generate complete formatted transition table
    table = ''
    table += header()
    for state in (state for state in states if state not in halting): # Omit rows for halting states
        table += filler_line() + line(state)
    table += footer()
    return table


def _get_tm_digraph(transition: TransitionTM, 
                    start: str, 
                    accept: str, 
                    reject: str,
                    filename: str | None = None) -> nx.DiGraph:
    '''
    - `transition`: transition object for TM
    - `start`: start state of TM, NOTE must be included in `transition` states (not checked)
    - `accept`: accept state of TM, NOTE must all be included in `transition` states (not checked)
    - `reject`: reject state of TM, NOTE must all be included in `transition` states (not checked)
    - `filename` (optional): name to be used to save image later if specified
    '''

    # Helper to get node colours
    # NOTE different to other models, due to unique reject state
    def get_node_col(state: str, 
                     accept_col: str = DEFAULT_ACCEPT_COL, 
                     reject_col: str = 'lightcoral', 
                     regular_col: str = DEFAULT_REJECT_COL) -> str:
        if state == accept: return accept_col
        elif state == reject: return reject_col
        else: return regular_col

    # Map (state, next_state) edges to respective label
    # Collect multiple transitions between the same states to single edge
    edge_label_map = {}
    for (state, letter), (next_state, write, direction) in transition.items():
        if (state, next_state) in edge_label_map:
            edge_label_map[(state, next_state)].append((letter, write, direction))
        else:
            edge_label_map[(state, next_state)] = [(letter, write, direction)]
    # Convert edge labels from lists of triples to formatted strings
    edge_label_map = {edge: get_edge_label_tm(label) for edge, label in edge_label_map.items()}

    # Create final digraph
    digraph = nx.DiGraph()
    # Add notes
    for state in transition.states:
        digraph.add_node(state, color = get_node_col(state))
    # Add edges
    for (state, next_state), label in edge_label_map.items():
        digraph.add_edge(state, next_state, label = label)
    # Add metadata
    digraph.graph['start'] = start
    digraph.graph['accept'] = accept
    digraph.graph['reject'] = reject
    digraph.graph['title'] = 'TM with ' + str(len(transition.states)) + ' states and input alphabet {' + ','.join(transition.input_alphabet) + '}'
    digraph.graph['kind'] = 'TM'
    digraph.graph['filename'] = filename
    return digraph
