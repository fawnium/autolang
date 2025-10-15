# Maximum length of edge label before abbreviating
# Includes all chars, not just number of letters
MAX_LABEL_LENGTH = 8

# Default colours for states in transition diagram
DEFAULT_ACCEPT_COL = 'lightgreen'
DEFAULT_REJECT_COL = 'lightgray'


# Layout to use for drawing digraph
DEFAULT_NETWORKX_LAYOUT = 'shell'

# Parameters for styling diagram

DEFAULT_NODE_SIZE = 700

DEFAULT_EDGE_CONNECTION_STYLE = 'arc3'

DEFAULT_EDGE_CURVATURE = 0.1

DEFAULT_EDGE_WIDTH = 1.0

DEFAULT_EDGE_ARROW_STYLE = None

DEFAULT_EDGE_ARROW_SIZE = 15

DEFAULT_NODE_FONT_SIZE = 12

DEFAULT_EDGE_FONT_SIZE = 10

# For formatting the text box of edge labels
EDGE_LABEL_BBOX = {
    'boxstyle': 'round,pad=0.1',
    'fc': 'white',
    'ec': 'black',
    'alpha': 1.0,
}