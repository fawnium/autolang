from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import os
from datetime import datetime



# Display matplotlib figure if GUI backend present
# Save as image if no GUI backend
def display_figure(fig: Figure, mode = None, path = None, filename = None):
    '''
    fig: matplotlib figure that plots transition diagram
    mode: either 'save' or 'inline'
        - if None, try to detect mode
    path: image location in case of save mode, excl filename
    filename: name to save image as e.g. 'diagram.png'
    '''
    if mode is None:
        mode = 'save' # TODO figure out how to detect GUI backend

    if mode == 'inline':
        plt.show()
    elif mode == 'save':
        # Determine save folder
        if path is None:
            os.makedirs('images', exist_ok=True) # Ensure save directory exists
            path = 'images/'
        # Determine filename
        if filename is None:
            # Default to just naming by the current time as 'HH_MM_SS'
            time_str = datetime.now().strftime("%H_%M_%S")
            filename = 'transition_diagram_' + time_str + '.png'
        # Save image
        fig.savefig(path + filename)
    else:
        raise ValueError(f'Unknown display mode \'{mode}\'')
