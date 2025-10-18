from autolang.visuals.settings_visuals import MAX_LABEL_LENGTH
from autolang.visuals.magic_chars import EPSILON, RIGHT_ARROW, ELLIPSIS

from collections.abc import Iterable, Sequence

# Convert '' to literal 'ε' for display
def eps(s: str) -> str:
    return s if s else EPSILON

# Helper to generate edge labels
# For NFAs and DFAs
def get_edge_label(letters: Sequence[str], 
                   max_length = MAX_LABEL_LENGTH) -> str:
    '''
    - `letters`: collection of letters to format into label, e.g. ['a','b','c'] -> 'a,b,c'
        - assumed to have no repeats
        - can include empty string
    - `max_length`: longest total length (in characters) before abbreviating label
    '''
    # Single string should not be passed directly
    # e.g. should 'abc' be interpreted as one letter of length 3, or 3 letters of length 1?
    if isinstance(letters, str):
        raise TypeError(f'Literal string \'{letters}\' must be wrapped in container.')

    letters = sorted(letters) # Ensure consistent order in label
    letters = [eps(letter) for letter in letters] # Convert '' to literal epsilon if present
    
    # Total length is sum of lengths of letters plus number of commas added
    # NOTE letters should all have length 1, so this is more for future-proofing
    length = sum(len(letter) for letter in letters) + (len(letters) - 1)
    # Join all letters by commas if total length short enough
    if length <= max_length:
        return ','.join(letters)
    # Only join some if total too long
    else:
        # Edge case for one letter
        if len(letters) == 1:
            # NOTE this block will only happen if a single 'letter' exceeds max length
            # This is very rare, and currently will never happen since all are length 1
            return letters[0]
        else:
            # Only include first and last, e.g. 'a,…,b'
            # NOTE probably smarter way to do this
            return letters[0] + ',' + ELLIPSIS + ',' + letters[-1]
    

# Get edge labels for PDA edge
def get_edge_label_pda(items: Iterable[tuple[str, str, str]], max_length = MAX_LABEL_LENGTH) -> str:
    '''
    - each `item` is (letter, stack_top, stack_push)
    - items get encoded as 'letter,stack_top->stack_push'
    - if multiple items, they are joined by newlines in accordance with Sipser
    '''
    items = sorted(items, key = lambda triple: triple[0]) # Sort only by 'letter'
    # Format items
    items = [(eps(letter) + ',' + eps(stack_top) + RIGHT_ARROW + eps(stack_push)) for (letter, stack_top, stack_push) in items]
    # TODO handle long length - length must be different to above case I think
    length = 0 # Placeholder
    if length <= max_length:
        return '\n'.join(items)
    else:
        pass


# Get edge labels for TM edge
def get_edge_label_tm(items: Iterable[tuple[str, str, str]], max_length = MAX_LABEL_LENGTH) -> str:
    '''
    - each `item` is (letter, write, direction)
    - items get encoded as 'letter->write,direction'
        - if write is same as letter, it's just 'letter->direction'
    - if multiple items, they are joined by newlines in accordance with Sipser
    '''
    # Helper to format single item
    def format_item(item: tuple[str, str, str]) -> str:
        if item[0] == item[1]:
            return item[0] + RIGHT_ARROW + item[2]
        return item[0] + RIGHT_ARROW + item[1] + ',' + item[2]
    items = sorted(items, key = lambda triple: triple[0]) # Sort only by 'letter'
    # Format items
    items = [format_item(item) for item in items]
    # TODO handle long length
    length = 0 # Placeholder
    if length <= max_length:
        return '\n'.join(items)
    else:
        pass