from autolang.backend.regex.regex_to_nfa import regex_to_nfa
from autolang.backend.regex.nfa_to_dfa import nfa_to_dfa

from autolang.backend.machines.dfa import DFA

# Just a wrapper of existing funcs for user convenience
def regex_to_dfa(regex: str) -> DFA:
    return nfa_to_dfa(regex_to_nfa(regex))