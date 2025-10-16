from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import networkx as nx

from autolang.visuals.settings_visuals import (DEFAULT_NETWORKX_LAYOUT,
                                               DEFAULT_NODE_SIZE,
                                               DEFAULT_EDGE_CONNECTION_STYLE,
                                               DEFAULT_EDGE_CURVATURE,
                                               DEFAULT_EDGE_WIDTH,
                                               DEFAULT_EDGE_ARROW_STYLE,
                                               DEFAULT_EDGE_ARROW_SIZE,
                                               DEFAULT_NODE_FONT_SIZE,
                                               DEFAULT_EDGE_FONT_SIZE,
                                               
                                               EDGE_LABEL_BBOX)

'''
Takes a digraph representing automaton, and generates a figure
- does *not* actually display the figure, see `display_diagrams.py`
'''


# Helper to get `pos` node coordinates
def get_pos(digraph: nx.DiGraph, layout: str | None) -> dict:
    # Catch None passed
    if layout is None: layout = DEFAULT_NETWORKX_LAYOUT
    # Dynamically choose layout algorithm
    layout_funcs = {
        'spring': nx.spring_layout,
        'shell': nx.shell_layout,
        'kamada_kawai': nx.kamada_kawai_layout,
        'circular': nx.circular_layout,
        #'spectral': nx.spectral_layout,
        #'planar': nx.planar_layout, # NOTE will often raise error!
        'spiral': nx.spiral_layout,
        'random': nx.random_layout
    }
    if layout not in layout_funcs:
        raise ValueError(f'\'{layout}\' is not a recognised layout.')
    # Maps nodes to coordinates in plot
    pos = layout_funcs[layout](digraph)
    return pos


# Return matplotlib figure with digraph on it
# Can either be later saved or shown inline directly
def render_digraph(digraph: nx.DiGraph, 
                   layout: str = DEFAULT_NETWORKX_LAYOUT,
                   *,
                   node_size: int = DEFAULT_NODE_SIZE,

                   edge_connection_style: str = DEFAULT_EDGE_CONNECTION_STYLE, # connectionstyle e.g. 'arc3'
                   edge_curvature: float = DEFAULT_EDGE_CURVATURE, # radius e.g. 0.2
                   edge_width: float | None = DEFAULT_EDGE_WIDTH,
                   edge_arrow_style: str | None = DEFAULT_EDGE_ARROW_STYLE,
                   edge_arrow_size: int = DEFAULT_EDGE_ARROW_SIZE,
                   
                   node_font_size: int = DEFAULT_NODE_FONT_SIZE,
                   edge_font_size: int = DEFAULT_EDGE_FONT_SIZE) -> Figure:

    # Dictionary mapping nodes to coordinates
    pos = get_pos(digraph, layout)

    # Specify edge curvature
    # e.g. 'arc3, rad=0.1'
    connectionstyle_str = edge_connection_style + ', rad=' + str(edge_curvature)

    # Create matplotlib figure
    fig, ax = plt.subplots()
    ax.set_axis_off() # Hide axes and grid
    fig.suptitle(digraph.graph['name']) # Show diagram title

    # Get node colours
    # Ensure colour order matches node order in digraph
    # NOTE default colour 'red' should never appear
    node_colors = [digraph.nodes[node].get('color', 'red') for node in digraph.nodes]

    # Make start state bold
    node_font_weights = {node: ('bold' if node == digraph.graph['start'] else 'normal') for node in digraph.nodes}

    # Draw each graph component to fig
    nx.draw_networkx_nodes(digraph, pos=pos, ax=ax, 
                           node_color=node_colors, 
                           edgecolors='black',

                           nodelist=None,
                           node_size=node_size,
                           node_shape='o',
                           alpha=None,
                           linewidths=None,
                           margins=None,
                           hide_ticks=True)
    
    nx.draw_networkx_edges(digraph, pos=pos, ax=ax, 
                           arrows=True,
                           connectionstyle=connectionstyle_str,
                           
                           edgelist=None,
                           width=edge_width,
                           edge_color='k',
                           style='solid',
                           alpha=None,
                           arrowstyle=edge_arrow_style,
                           arrowsize=edge_arrow_size,

                           node_size=node_size,
                           nodelist=None,
                           node_shape='o',
                           hide_ticks=True)
    
    nx.draw_networkx_labels(digraph, pos=pos, ax=ax,
                            labels=None,
                            font_size=node_font_size,
                            font_color='k',
                            font_weight=node_font_weights, # Could use for start state?
                            font_family='sans-serif',
                            
                            alpha=None,
                            bbox=None,
                            horizontalalignment='center',
                            verticalalignment='center',
                            
                            clip_on=True,
                            hide_ticks=True)

    edge_labels = nx.get_edge_attributes(digraph, 'label') # Extract edge labels into dict
    nx.draw_networkx_edge_labels(digraph, pos=pos, ax=ax, 
                                 edge_labels=edge_labels,
                                 connectionstyle=connectionstyle_str,

                                 label_pos=0.5,
                                 font_size=edge_font_size,
                                 font_color='k',
                                 font_weight='normal',
                                 font_family='sans-serif',
                                 
                                 alpha=None,
                                 bbox=EDGE_LABEL_BBOX, # NOTE probably important
                                 horizontalalignment='center',
                                 verticalalignment='center',
                                 rotate=False,

                                 node_size=node_size,
                                 nodelist=None,

                                 clip_on=True,
                                 hide_ticks=True)
    return fig

