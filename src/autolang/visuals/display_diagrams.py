from matplotlib import get_backend
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import os
from datetime import datetime

'''
Takes existing figure, and either displays it or saves it as an image.

NOTE this file is a complete mess

See:
https://matplotlib.org/stable/users/explain/figure/backends.html
https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
https://stackoverflow.com/questions/32538758/nameerror-name-get-ipython-is-not-defined
'''

# Determine matplotlib backend
def get_matplotlib_backend() -> str:
    return get_backend().lower()


# Try determine if in ipython environment
def is_ipython() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell': # Jupyter notebook
            return True
        elif shell == 'TerminalInteractiveShell': # IPython terminal
            return True
        else:
            return False
    except ImportError:
        return False
    except Exception:
        return False
    

# Try to determine if a gui backend exists, i.e. whether `plt.show()` won't raise an error
# NOTE likely very brittle
def can_call_plt_show() -> bool:
    # Some backends that should work
    interactive_backends = {'qtagg',
                            'ipympl',
                            'gtk3agg',
                            'gtk4agg',
                            'macosx',
                            'tkagg',
                            'nbagg',
                            'webagg',
                            'gtk3cairo',
                            'gtk4cairo',
                            'wxagg'}
    if get_matplotlib_backend() in interactive_backends:
        return True
    # Assume possible in ipython
    if is_ipython():
        return True
    return False # May have false negatives
    
# Generate default filename for image if none given
def get_filename() -> str:
    # Default to just naming by the current time as 'HH_MM_SS'
        time_str = datetime.now().strftime("%H_%M_%S")
        filename = 'transition_diagram_' + time_str + '.png'
        return filename


# Display matplotlib figure if GUI backend present
# Save as image if no GUI backend
def display_figure(fig: Figure, 
                   mode: str | None = None, 
                   filename: str | None = None):
    '''
    fig: matplotlib figure that plots transition diagram
    mode: either 'save' or 'show'
        - if None, try to detect mode
    filename: name to save image as e.g. 'diagram.png'
    '''
    # Try to auto-detect best mode
    if mode is None:
        if can_call_plt_show():
            mode = 'show'
        else:
            mode = 'save'
        
    if mode == 'show':
        # Warning message for users in case broken
        print('WARNING: plotting diagrams is a work in progress, and may not work.')
        print('Use `mode = \'save\'` as an argument to save an image instead.')
        print('Report a problem with plotting at `https://github.com/fawnium/autolang`')
        # Final error catch just in case
        try:
            plt.show()
        except Exception as e:
            print(f'Unable to show plot: {e}')

    elif mode == 'save':
        # Ensure save directory exists
        os.makedirs('images', exist_ok=True)
        # Determine filename
        if filename is None:
            filename = get_filename()
        # Save image
        fig.savefig('images/' + filename)

    else:
        raise ValueError(f'Unknown display mode \'{mode}\'')
