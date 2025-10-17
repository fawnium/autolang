from autolang.backend.machines.structs_transition import TransitionPDA
from autolang.visuals.magic_chars import V, H, UL, UR, DL, DR, UDL, UDR, ULR, DLR, UDLR, EPSILON, EMPTY
from autolang.visuals.settings_visuals import DEFAULT_ACCEPT_COL, DEFAULT_REJECT_COL
from autolang.visuals.utils_visuals import get_edge_label_pda

from collections.abc import Iterable

import networkx as nx


# Helpers to format list of next configs as a table entry

# NOTE only for transition table, not transition diagram
def config_to_str(config: tuple[str, str]) -> str:
    return '(' + config[0] + ',' + (config[1] if config[1] else EPSILON) + ')' # Turn tuple into str and convert '' into 'ε'

# NOTE only for transition table, not transition diagram
def next_configs_to_str(configs: tuple[tuple[str, str], ...]) -> str:
    if not configs: return ' ' # Case where no next configs # NOTE should we do ' ' or EMPTY for readability?
    configs = sorted(configs, key=lambda conf: (len(conf[0]), conf[0], conf[1])) # Sort list of configs with priority: length of state > lex of state > lex of letter
    return '{' + ','.join(config_to_str(config) for config in configs) + '}'

def _transition_table_pda(transition: TransitionPDA):
    # Titles for top-left corner
    title_input = 'Input:'
    title_stack = 'Stack:'
    # Unpack states and alphabets
    states = transition.states
    input_alphabet = transition.input_alphabet
    stack_alphabet = transition.stack_alphabet
    '''
    NOTE MICRO and MACRO columns
    - micro columns are the finest cols which are one cell wide, and correspond to single STACK letter in header
    - macro columns correspond to a single INPUT letter
        - each macro col has one micro col PER stack letter (incl. epsilon)
    '''
    macro_letters = input_alphabet + ('',) # Include epsilon in alphabet for cleaner iteration
    micro_letters = stack_alphabet + ('',)
    first_stack_letter = micro_letters[0] # For identifying start of macro cell

    # Calculate widths
    # NOTE here widths are col-specific (unlike DFA/NFA), because there are far more cols
    width_header = max(len(title_input), len(title_stack), max(len(state) for state in states)) # Width of leftmost header col
    widths_micro = {} # Width of each micro col - one width for each letter-stack pair
    for letter, stack_top in ((letter, stack_top) for letter in macro_letters for stack_top in micro_letters):
        width = max(len(next_configs_to_str(transition.get((state, letter, stack_top)))) for state in states) # Longest next configs str for particular micro col
        width = max(width, len(letter), len(stack_top)) # Account for header entries being longer than cells
        widths_micro[(letter, stack_top)] = width # Set col width to retrieve below

    # Helper to pad cells
    def cell(s: str, width: int) -> str:
        return s + (' ' * (width - len(s)))
    
    # Print top border and macro header of input letters
    def print_macro_header():
        div_line = DR + (H * width_header) # Top border line
        line = V + cell(title_input, width_header) # Macro header line
        # Build both lines in single loop
        for letter in macro_letters:
            for stack_top in micro_letters:
                if stack_top == first_stack_letter: # Case for first micro col
                    div_line += DLR + (H * widths_micro[((letter, stack_top))])
                    line += V + cell(letter if letter else EPSILON, widths_micro[((letter, stack_top))])
                else: # Case for all other micro cols
                    div_line += H * (1 + widths_micro[((letter, stack_top))])
                    line += ' ' * (1 + widths_micro[((letter, stack_top))])
        # Final border
        div_line += DL
        line += V
        # Print lines
        print(div_line)
        print(line)

    # Print line between macro and micro headers, and micro header of stack letters
    def print_micro_header():
        div_line = UDR + (H * width_header) # Line between headers
        line = V + cell(title_stack, width_header) # Micro header line
        # Build both lines in single loop
        for letter in macro_letters:
            for stack_top in micro_letters:
                if stack_top == first_stack_letter: # Case for first micro col - must join with div above
                    div_line += UDLR + (H * widths_micro[(letter, stack_top)])
                else: # Case for other micro cols - must only join div below
                    div_line += DLR + (H * widths_micro[(letter, stack_top)])
                line += V + cell(stack_top if stack_top else EPSILON, widths_micro[(letter, stack_top)])
        # Final border
        div_line += UDL
        line += V
        # Print lines
        print(div_line)
        print(line)
    
    # Print line between table rows
    def print_filler_line():
        line = UDR + (H * width_header) # Start line with border and header cell
        for letter in macro_letters:
            for stack_top in micro_letters:
                line += UDLR + (H * widths_micro[((letter, stack_top))]) # Add each micro col one by one
        line += UDL # Add final border
        print(line)

    # Print row of entries in table
    def print_line(state: str):
        line = V + cell(state, width_header) # Start with border and header cell
        for letter in input_alphabet + ('',):
            for stack_top in stack_alphabet + ('',):
                next_config = transition.get((state, letter, stack_top)) # Get each cell entry
                line += V + cell(next_configs_to_str(next_config), widths_micro[(letter, stack_top)]) # Add each cell one by one (incl. right div)
        line += V # Add final border
        print(line)

    # Print bottom border
    def print_footer():
        line = UR + (H * width_header) # Start with corner and header cell
        for letter in macro_letters:
            for stack_top in micro_letters:
                line += ULR + (H * widths_micro[(letter, stack_top)]) # Add each border section one by one
        line += UL # Add final corner
        print(line)

    # Print formatted transition table
    print_macro_header()
    print_micro_header()
    for state in states:
        print_filler_line()
        print_line(state)
    print_footer()


def _get_pda_digraph(transition: TransitionPDA, start: str, accept: Iterable[str]) -> nx.DiGraph:

    # Helper to determine node colour
    def get_node_col(state: str, accept_col: str = DEFAULT_ACCEPT_COL, reject_col: str = DEFAULT_REJECT_COL) -> str:
        return accept_col if state in accept else reject_col
    
    # Map (state, next_state) edges to respective label
    # Collect letters + stack pushes into single edge between the same states
    edge_label_map = {}
    for (state, letter, stack_top), next_configs in transition.items():
        for (next_state, stack_push) in next_configs:
            if (state, next_state) in edge_label_map:
                edge_label_map[(state, next_state)].append((letter, stack_top, stack_push))
            else:
                edge_label_map[(state, next_state)] = [(letter, stack_top, stack_push)]
    # Convert edge labels from lists of triples to formatted strings
    edge_label_map = {edge: get_edge_label_pda(label) for edge, label in edge_label_map.items()}
    
    # Create final DiGraph
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
    digraph.graph['name'] = 'PDA with ' + str(len(transition.states)) + ' states, input alphabet {' + ','.join(transition.input_alphabet) + '}, stack {' + ','.join(transition.stack_alphabet) + '}'
    digraph.graph['kind'] = 'PDA'
    return digraph

