from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx

from autolang.visuals.settings_visuals import DEFAULT_NETWORKX_LAYOUT

'''
Takes a digraph representing automaton, and generates a figure
- does *not* actually display the figure, see `display_diagrams.py`
'''


# Return matplotlib figure with digraph on it
# Can either be later saved or shown inline directly
def render_digraph(digraph: nx.DiGraph, 
                   layout: str = DEFAULT_NETWORKX_LAYOUT) -> Figure:

    # Dynamically choose layout algorithm
    layout_funcs = {
        'spring': nx.spring_layout,
        'shell': nx.shell_layout,
        'kamada_kawai': nx.kamada_kawai_layout,
        'circular': nx.circular_layout,
        'spectral': nx.spectral_layout,
        'planar': nx.planar_layout, # NOTE will often raise error!
        'spiral': nx.spiral_layout,
        'random': nx.random_layout
    }
    if layout not in layout_funcs:
        raise ValueError(f'\'{layout}\' is not a recognised layout.')
    # Maps nodes to coordinates in plot
    pos = layout_funcs[layout](digraph)

    # Create matplotlib figure
    fig, ax = plt.subplots()
    ax.set_axis_off() # Hide axes and grid
    fig.suptitle(digraph.graph['name']) # Show diagram title

    # Get node colours
    # Ensure colour order matches node order in digraph
    # NOTE default colour 'red' should never appear
    node_colors = [digraph.nodes[node].get('color', 'red') for node in digraph.nodes]

    # Draw each graph component to fig
    nx.draw_networkx_nodes(digraph, pos=pos, ax=ax, 
                           node_color=node_colors, 
                           edgecolors='black')
    nx.draw_networkx_edges(digraph, pos=pos, ax=ax, 
                           arrows=True,
                           connectionstyle='arc3, rad=0.1')
    nx.draw_networkx_labels(digraph, pos=pos, ax=ax)
    edge_labels = nx.get_edge_attributes(digraph, 'label') # Extract edge labels into dict
    nx.draw_networkx_edge_labels(digraph, pos=pos, ax=ax, edge_labels=edge_labels)

    return fig

