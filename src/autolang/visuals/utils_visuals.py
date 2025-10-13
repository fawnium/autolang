from autolang.visuals.settings_visuals import MAX_LABEL_LENGTH
from collections.abc import Iterable

# Helper to generate edge labels
def get_edge_label(letters: Iterable[str], max_length = MAX_LABEL_LENGTH) -> str:
    letters = sorted(letters)
    # Total length is sum of lengths of letters plus number of commas added
    length = sum(len(letter) for letter in letters) + (len(letters) - 1)
    # Join all letters by commas if total length short enough
    if length <= max_length:
        return ','.join(letters)
    # Only join some if total too long
    else:
        # TODO handle edge case where only one letter?
        # TODO not just start and end, but as many as possible while still under max length?
        return letters[0] + ',...,' + letters[-1]