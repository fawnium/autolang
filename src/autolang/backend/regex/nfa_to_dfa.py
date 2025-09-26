from autolang.backend.machines.dfa import DFA
from autolang.backend.machines.nfa import NFA
from collections.abc import Iterable

# Object that handles subset construction of a DFA from an NFA
class ConstructDFA:

    def __init__(self, nfa: NFA):
        self.nfa = nfa

    # Helper to create a unique, sorted, ordered, canonical representation of subsets
    # In particular ensures hashability
    def subset_to_tuple(self, states: Iterable[str]) -> tuple[str, ...]:
        return tuple(sorted(states, key=lambda s: (len(s), s))) # Sort states in len-lex order and convert to tuple

    # Helper to encode set of states into single string to pass to DFA object - e.g. '{state1, state2, state3}'
    def subset_to_str(self, states: Iterable[str]) -> str:
        return '{' + ','.join(sorted(states, key=lambda s: (len(s), s))) + '}' # Ensure states appear in len-lex order with sorting key for the set

    # Close list of states by recursively including all epsilon transitions
    def epsilon_closure(self, states: set[str]) -> set[str]:
        '''
        - Iteratively add states yielded by epsilon-transitions
        - Use a queue to keep track of paths to explore for new states to add, similar to `NFA.compute()` in nfa.py
        '''
        closure = set(states) # All states to be returned
        queue = list(states) # Queue of states to explore e-transitions from
        while queue:
            current = queue.pop()
            new_states = self.nfa.transition.get((current, '')) # Get new potential states in closure via nfa ε-transitions, NOTE will return empty list if no transitions (I hope)
            for new_state in new_states:
                if new_state in closure:
                    continue # Nothing to do if state already added, move on to next `new_state` to avoid infinite loops
                else:
                    closure.add(new_state)
                    queue.append(new_state) # Remember to explore new transitions starting at this state
        return closure

    # Construct temporary transition function of DFA
    def construct(self) -> dict[tuple[tuple[str, ...], str], tuple[str, ...]]:
        '''
        Build DFA transition function using lazy subset construction
        - initialise empty transition dict
        - initiliase `visited` set of dfa-states from which transitions (for ALL letters) have already been added
        - initialise `queue` of dfa-states to add transitions from
            - NOTE dfa-states in the `queue` have already been epsilon-closed
        - while still states to populate:
            - iterate over all nfa-states in dfa-state, and all alphabet letters
            - get each transition from nfa
            - if transition leads to dfa-state already visited, just add the transition and continue
            - elif transition leads to new dfa-state, add it and then add destination dfa-state to queue
        '''
        dfa_transition = dict() # Initialise temporary transition function to be built - format is dict[tuple[str, str], set[str]]
        visited = set() # Set of dfa-states for which all transitions have already been added, NOTE members must be in canonical form via `subset_to_tuple()`!
        start_state = self.epsilon_closure({self.nfa.start}) # Initial dfa-state, NOTE nfa start state must be wrapped inside a set! See `epsilon_closure()` above
        queue = [self.subset_to_tuple(start_state)] # Queue of dfa-states to add transitions from
        while queue:
            dfa_current = queue.pop() 
            # For each alphabet letter, build union of nfa-states to yield transition to next dfa-state - see Sipser p55 near the bottom of the page
            for letter in self.nfa.alphabet:
                dfa_next = set() # New set of nfa-states reachable via any state in dfa_current and current letter
                for nfa_state in dfa_current:
                    dfa_next.update(self.nfa.transition.get((nfa_state, letter))) # Add all new nfa-states reachable from current dfa-state, NOTE using set enforces no repeats
                dfa_next = self.epsilon_closure(dfa_next) # Include all ε-transitions
                dfa_next = self.subset_to_tuple(dfa_next) # Convert to canonical form to ensure fixed order of nfa-states and hashability
                # If the union just built is a new subset, add to queue to explore transitions starting from it
                if dfa_next not in visited:
                    queue.append(dfa_next)
                visited.add(dfa_next) # Convert to list to be added to set, and sort to ensure no duplicates of same subset
                # Add the transition itself
                # NOTE the (dfa_current, letter) key will be unique and not already exist, because of how this code performs lazy construction, so each pair will only be seen once
                dfa_transition[(dfa_current, letter)] = dfa_next # NOTE empty next state is allowed, and will be set if no transitions for any state or letter in NFA
        return dfa_transition

    def to_dfa(self):
        temp_transition = self.construct() # Build transition, with states as sets instead of strings temporarily
        # Convert states inside transition dict from tuples to strings
        transition = {(self.subset_to_str(state), letter): self.subset_to_str(next_state) for (state, letter), next_state in temp_transition.items()}
        start = self.subset_to_str(self.epsilon_closure({self.nfa.start})) # DFA start state is epsilon closure of NFA start state
        # Determine accept states by comparing to NFA states and checking for intersection - much easier to do before dfa-states get string-ified
        accept_set = set()
        for (dfa_state, _), dfa_next_state in temp_transition.items():
            # If any nfa-state inside dfa-state is an accept, then dfa-state becomes an accept
            for nfa_state in dfa_state:
                if nfa_state in self.nfa.accept:
                    accept_set.add(dfa_state)
                    break
            for nfa_state in dfa_next_state:
                if nfa_state in self.nfa.accept:
                    accept_set.add(dfa_next_state)
                    break
        accept = sorted([self.subset_to_str(dfa_state) for dfa_state in accept_set], key=lambda s: (len(s), s)) # String-ify and sort final accept states
        return DFA(transition, start, accept)

# Carries out state-minimisation to optimise existing DFA
def minimise_dfa(dfa: DFA) -> DFA:
    raise NotImplementedError

# Wrapper for above construction
def nfa_to_dfa(nfa: NFA) -> DFA:
    return ConstructDFA(nfa).to_dfa()