from autolang.backend.regex.regex_input import is_valid_regex, add_concat
from autolang.backend.regex.gnfa import GNFA
from autolang.backend.machines.nfa import NFA

# Convert input regex to NFA object - glues together everything regex.py, regex_eliminate.py, gnfa.py
def regex_to_nfa(regex: str) -> NFA:
    if not is_valid_regex(regex):
        raise ValueError(f'Input regex \'{regex}\' is invalid. Please check regex syntax.')
    regex = add_concat(regex)
    gnfa = GNFA(regex)
    return gnfa.to_nfa()