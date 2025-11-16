from autolang.backend.utils import disjoint_symbol, _append_dict_value
from autolang.visuals.utils_visuals import eps

from collections.abc import Iterable, Generator, Sequence, Callable

'''
Context-Free Grammar Class

NOTE naming conventions in this file:

'symbol': any string appearning in CFG, i.e. a letter, either terminal or nonterminal
'nonterminal': symbol that is the head of a rule, a.k.a. variable
'terminal': symbol that is not a nonterminal, i.e. appears in a final derived word

'rule': ordered pair where first element is a nonterminal, and second is a sequence of symbols (i.e. body)
'rules': collection of all rules in CFG

'head': nonterminal when it is first element of a rule
'body': sequence of symbols as the second element of rule, a.k.a 'rule body'
'bodies': collection of all rule bodies *for specific nonterminal*

'unit rule': rule whose body is a single symbol that is a **nonterminal**
    - NOTE in particular, if body is a terminal then it is not a unit rule

'compound rule': rule with body length more than 1 (non-standard term I believe)

'e-rule': rule whose body is the empty symbol '', a.k.a. 'ε-rule', 'epsilon-rule'
'bad e-rule': e-rule whose head is not the start nonterminal

'''

# Type alias for canonical rules map
# Maps nonterminal strings to tuple of respective rule bodies
# Each individual body is a tuple of strings
RulesMap = dict[str, tuple[tuple[str, ...], ...]]


class CFG:

    def __init__(self,
                 rules: dict[str, Iterable[Sequence[str] | str]],
                 start: str):
        '''
        Params
        - `rules`: maps each nonterminal to collection of all its rule bodies
            - each body is either a single string or sequence of strings
            - NOTE a single string is interpreted as ONE symbol, NOT a sequence of symbols
        - `start`: start nonterminal, must be included in rules
        '''
        # Convert rules to standard form
        self.rules = CFG._canonise_rules(rules)
        
        # Check start is listed as a nonterminal
        if start not in rules:
            raise ValueError(f'Start nonterminal \'{start}\' must be listed in rules.')
        self.start = start

        # Extract symbol sets
        self.nonterminals, self.terminals = CFG._extract(self.rules)

    '''
    INPUT HANDLING
    '''
        
    # Ensure rules dict is correctly formatted and convert containers to tuples for consistency
    @staticmethod
    def _canonise_rules(rules: dict[str, Iterable[Sequence[str] | str]]) -> RulesMap:
        '''
        Params
        - `rules`: rules map, may not be in canonical form

        Overview
        Convert rules map with flexible types and formatting into strict canonical form:
        - for each nonterminal, bodies is a tuple
            - empty bodies tuple IS allowed (for when nonterminal has no rules)
            - bodies can be unordered
            - NOTE string is NOT allowed as bodies, despite being Iterable
        - within bodies, each body is a tuple of strings/symbols
            - in particular, body that is a single string is wrapped in a tuple, including e-rule
            - empty body NOT allowed in canonical form
                - the correct way to encode an e-rule is as the single-symbol tuple ('',)
            - body must be ordered
        - '' not allowed as a nonterminal
        - '' only allowed in body if it is the only symbol (i.e. e-rule)


        Implementation
        - for each `head`: `bodies` pair in rules map:
            - ensure head is a non-empty string
            - ensure body is a non-string iterable
            - for each `body` in bodies:
                - if body is string, wrap as 1-tuple to canonise
                - if body is non-string sequence:
                    - ensure all elements are strings
                    - if empty, assume e-rule intended, canonise as ('',)
                    - if length >1, ensure '' not present as element
                    - canonise by converting to tuple
            - ensure no duplicate bodies after canonising
            - sort bodies in lenlex order
            - convert bodies to parent tuple
            - assign bodies to head's key in final dict
        - return canonical dict

        Return
        - canonised rules map dict
        '''
        if not isinstance(rules, dict):
            raise TypeError('CFG rules must be a dict mapping nonterminals to rule bodies.')

        canonical = {} # Initialise canonical dict

        for head, bodies in rules.items():

            if not isinstance(head, str):
                raise TypeError(f'Nonterminal \'{head}\' must be a string.')
            # '' Cannot be a nonterminal
            if not head:
                raise ValueError('Empty string \'\' not allowed as a nonterminal.')

            if not isinstance(bodies, Iterable):
                raise TypeError(f'Rule bodies for nonterminal \'{head}\' must be iterable.')
            # String as value not allowed (TODO allow if unambiguous?)
            if isinstance(bodies, str):
                raise TypeError(f'Rule bodies \'{bodies}\' must be iterable of strings, not single string.')
            
            canonical_bodies = [] # Bodies to be converted, final type will be tuple[tuple[str, ...]]

            for body in bodies:
                if isinstance(body, str):
                    # NOTE using tuple() directly would separate chars into individual entries, which is not intended
                    canonical_bodies.append((body,))

                # NOTE in this case body will not be a string, since that is caught in above case
                elif isinstance(body, Sequence):
                    # Ensure all strings
                    if not all(isinstance(symbol, str) for symbol in body):
                        raise TypeError('All terminals and nonterminals must be strings.')
                    
                    # Convert empty body to ('',)
                    if not body:
                        body = ('',)
                    
                    # Ensure no '' in compound rule
                    if len(body) > 1 and '' in body:
                        raise ValueError(f'Empty symbol \'\' not allowed in non-unit rule.')

                    canonical_bodies.append(tuple(body))

                else:
                    raise TypeError(f'Rule body \'{body}\' must be an ordered sequence of strings.')
            
            # Remove duplicate bodies, sort by lenlex, convert to tuple
            canonical[head] = tuple(sorted(set(canonical_bodies), key=lambda body: (len(body), body)))
        return canonical

    # Establish terminals and nonterminals from rules
    @staticmethod
    def _extract(rules: RulesMap) -> tuple[tuple[str, ...], tuple[str, ...]]:
        '''
        Params
        - `rules`: canonised rules map to get symbols from

        Overview
        Determine which symbols are nonterminals and terminals, return both collections as ordered tuples
        - nonterminals are precisely the keys of the dict
        - terminals are all other symbols excluding ''
        - NOTE for a nonterminal 'A' to be identified as such, it must be included as `'A': tuple()` in dict,
          otherwise it will be assumed a terminal

        Implementation
        - initialise nonterminals and terminals as sets (prevents duplicates)
        - for each `head`: `bodies` in rules:
            - add head to nonterminals
            - for each body in bodies:
                - add each symbol in body to terminals
        - filter out nonterminals and '' from terminals to leave only true terminals
        - sort nonterminals and terminals, convert to tuples
        - return both

        Return 
        - (nonterminals, terminals)
        '''
        nonterminals = set()
        terminals = set()

        # Extract symbols from rules dict
        for head, bodies in rules.items():
            nonterminals.add(head)
            for body in bodies:
                for symbol in body:
                    terminals.add(symbol)

        # Filter nonterminals and empty symbol '' out of terminals
        terminals = {symbol for symbol in terminals if symbol not in nonterminals and symbol}

        # Sort symbols and convert to tuple
        # TODO make these sets?
        return tuple(sorted(nonterminals)), tuple(sorted(terminals))
    
    '''
    DUNDERS
    '''
    
    def __repr__(self):
        repr_str = 'CFG(\n'
        # Iterate such that start nonterminal appears first
        for head, bodies in ((self.start, self.rules[self.start]),) + tuple(item 
                                                                                          for item in self.rules.items() 
                                                                                          if item[0] != self.start):
            repr_str += head + ' ::= '
            repr_str += ' | '.join(' '.join(eps(symbol) for symbol in body) for body in bodies)
            repr_str += '\n'
        repr_str += ')'
        return repr_str
    
    def __str__(self):
        return 'CFG with nonterminals {' + ','.join(self.nonterminals) + '} and terminals {' + ','.join(self.terminals) + '}'
    
    '''
    NAME GENERATION HELPERS
    '''

    # For Chomsky normal form, removing rules with body length > 2
    @staticmethod
    def _new_nonterminals_chomsky_chain(initial_nonterminal: str,
                                        rule_index: int,
                                        chain_length: int) -> tuple[str, ...]:
        '''
        Params
        - `initial_nonterminal`: head of rule being eliminated
        - `rule_index`: number of rule being eliminated in list of head's long rules
        - `chain_length`: number of new nonterminals required (length of body minus 2)

        Overview
        Generate tuple of new nonterminal names, specifically for elminating rules with body length > 2.
        
        Each new nonterminal is of the form '#CHAIN_A_i_j' where:
        - 'A' is the initial nonterminal for which long rule being eliminated
        - 'i' indexes all of 'A's rules with length > 2, as a subsequence of 'A's total rules
        - 'j' is the index of the specific new nonterminal within a given elimination
        
        Examples

        If 'A' has only one rule with body length > 2, 'A -> a1 a2 ... an', the new nonterminals are:

        '#CHAIN_A_1_1', '#CHAIN_A_1_2', ..., '#CHAIN_A_1_{n-2}'

        If 'A' has two rules with body length > 2, 'A -> a1 a2 ... an' and 'A -> b1 b2 ... bm', new nonterminals are:

        '#CHAIN_A_1_1', '#CHAIN_A_1_2', ..., '#CHAIN_A_1_{n-2}'
        '#CHAIN_A_2_1', '#CHAIN_A_2_2', ..., '#CHAIN_A_2_{m-2}'

        These would come from two separate calls of this method.

        NOTE the rule bodies for all nonterminals are in lenlex order, so index 'i' is deterministic.

        NOTE the '#CHAIN_' prefix is to make accidental name collisions less likely.
        
        Return
        - tuple of new nonterminals for a specific rule elimination
        '''
        new_nonterminals = tuple(f'#CHAIN_{initial_nonterminal}_{rule_index}_{j}'
                                 for j in range(1, chain_length + 1))
        return new_nonterminals
        

    '''
    UNION - TODO WIP
    '''
    
    # Rename symbols in CFG
    # TODO better collision checking
    # TODO only pass rules map not CFG?
    @staticmethod
    def _rename_symbols(cfg: 'CFG', rename_map: dict[str, str]) -> 'CFG':
        '''
        - `rename_map`: keys are current nonterminals, values are the corresponding renamed nonterminals
        
        Change every symbol instance in rules to its image under rename_map
        - this applies to both heads and instances within rule bodies
        - NOTE this function can be used to rename terminals for generality, but is only intended for nonterminals
        - if a symbol does not have an image in rename_map, it stays the same
        '''
        # Ensure no collision between renamed nonterminals and existing terminals
        if any(symbol in cfg.terminals for symbol in rename_map.values()):
            raise ValueError('Renamed nonterminal collides with existing terminal.')

        new_rules = {}
        
        for head, bodies in cfg.rules.items():
            new_bodies = []
            for body in bodies:
                # Rename each symbol in body, add to list of renamed bodies
                # Default to original name
                new_bodies.append(tuple(rename_map.get(symbol, symbol) for symbol in body))
            new_rules[rename_map.get(head, head)] = tuple(new_bodies)

        return CFG(new_rules, rename_map.get(cfg.start, cfg.start))


    # Return CFG whose language is the union of the languages of self and other
    # NOTE can only form union where terminals are equal, TODO allow different terminal sets
    # TODO better collision checks!
    def union(self, other: 'CFG') -> 'CFG':
        '''
        Form union of two CFGs by adding a new start symbol S and rule S -> S_1 | S_2
        - ensure other object is a valid CFG
        - ensure terminal alphabets match (NOTE may drop this later)
        - rename nonterminals by appending '_1' for self and '_2'
            - this necessarily prevents name collisions, and also tracks origin grammar
        - create new start symbol
        - form union of rules from both grammars (guaranteed disjoint from above)
        - add rules so new start symbol can yield both original start symbols
        - return new grammar
        '''
        # Check input
        if not isinstance(other, CFG):
            raise TypeError(f'Object \'{other}\' must be a CFG.')
        
        # Check nonterminals match
        '''
        TODO enable differing nonterminal sets - needs more complex collision checking

        - The reason to ensure alphabets are the same is in case a nonterminal in one CFG doesn't collide with a terminal 
          in the other
        - e.g. if `self` has a nonterminal 'R' and `other` has a terminal 'R_1', then after renaming nonterminals there will be a collision
            - This would mean 'R_1' would always be treated as a nonterminal during symbol extraction, so effectively it would be dropped from 
              the set of terminals
            - Such an example is rare (users likely won't use '_i' as a terminal name over single chars), but could still technically happen, 
              so for now it's just banned

        TODO there are still possible collisions I think
        '''
        if set(self.terminals) != set(other.terminals):
            raise ValueError('Can only form union where CFGs have the same terminals.')
        
        # Add indices to all nonterminal names
        rename_self = {nonterminal: nonterminal + '_1' for nonterminal in self.nonterminals}
        renamed_self = CFG._rename_symbols(self, rename_self)

        rename_other = {nonterminal: nonterminal + '_2' for nonterminal in self.nonterminals}
        renamed_other = CFG._rename_symbols(other, rename_other)
        
        # Generate new start nonterminal that is not present as a symbol anywhere in either initial CFG
        new_start = disjoint_symbol('S', set(renamed_self.nonterminals) | 
                                         set(renamed_self.terminals) | 
                                         set(renamed_other.nonterminals) | 
                                         set(renamed_other.terminals))

        # Form union of rules of both CFGs
        new_rules = {head: bodies for head, bodies in renamed_self.rules.items()}
        for head, bodies in renamed_other.rules.items():
            new_rules[head] = bodies

        # Add start rule
        new_rules[new_start] = ((renamed_self.start,), (renamed_other.start,))

        return CFG(new_rules, new_start)
    
    '''
    CHOMSKY NORMAL FORM
    '''

    # Return new tuple of bodies with given `target` removed
    @staticmethod
    def _delete_body_from_bodies(target: tuple[str, ...], 
                                 bodies: tuple[tuple[str, ...], ...]) -> tuple[tuple[str, ...], ...]:
        '''
        Params
        - `target`: rule body to remove
        - `bodies`: bodies to remove target from

        Overview
        Remove specific rule body from a nonterminal's bodies
        - raise error if target not found, since in that case method shouldn't have been called

        Return
        - new bodies tuple with target deleted
        '''
        if target not in bodies:
            raise ValueError(f'Rule body \'{target}\' not present in tuple, cannot delete.')

        return tuple(body for body in bodies if body != target)
    
    # General rule filtering helper, used by below methods
    @staticmethod
    def _filter_bodies(rules: RulesMap,
                       condition: Callable[[tuple[str, ...]], bool]) -> RulesMap:
        '''
        Params
        - `rules`: rules map to filter
        - `condition`: statement about a rule body to filter by

        Overview
        Return new rules map that only contains rules whose body satisfies given condition
        - `condition` should be a function whose input is a rule body that outputs a bool
            - e.g. a lambda function
        - Rules in filtered map are precisely those whose body returns True for condition

        Return
        - new rules map filtered to only contain rules whose body satisfies given condition
        '''
        # Initialise return dict
        filtered_rules = {}

        for head, bodies in rules.items():
            for body in bodies:
                if condition(body):
                    _append_dict_value(head, body, filtered_rules)

        # Convert lists to tuples for return
        filtered_rules = {head: tuple(bodies) for head, bodies in filtered_rules.items()}
        return filtered_rules


    # Return all rules that contain given symbol in body
    @staticmethod
    def _get_bodies_containing(target: str,
                               rules: RulesMap) -> RulesMap:
        '''
        Params
        - `target`: symbol to query presence of within rule bodies
        - `rules`: rules map to query

        Return
        - new rules map filtered to only contain rules where target symbol occurs in body
        '''
        filtered_rules = CFG._filter_bodies(rules,
                                            lambda body: target in body)

        # Raise error if no occurences - likely invalid symbol
        if not filtered_rules:
            raise ValueError(f'Symbol \'{target}\' not found in any rule body.')

        return filtered_rules
    
    # Return all rules with body of specified length
    # TODO handle e-rules, should they be considered length 0 or 1? Currently 1
    @staticmethod
    def _get_bodies_of_length(length: int,
                              rules: RulesMap) -> RulesMap:
        '''
        Params
        - `length`: length of rule bodies to filter by
        - `rules`: rules map to query

        Return
        - new rules map filtered to only contain rules with body of given length
        '''
        filtered_rules = CFG._filter_bodies(rules,
                                            lambda body: len(body) == length)

        return filtered_rules
    
    # Return all rules with body of length greater than specified length
    @staticmethod
    def _get_bodies_length_greater_than(length: int,
                                        rules: RulesMap) -> RulesMap:
        '''
        Params
        - `length`: length of rule bodies to filter by
        - `rules`: rules map to query

        Return
        - new rules map filtered to only contain rules with body of given length
        '''
        filtered_rules = CFG._filter_bodies(rules,
                                            lambda body: len(body) > length)

        return filtered_rules
                
    
    # Insert new collection of rules to existing rules map
    # NOTE ONLY for adding new rules for existing nonterminals, NOT for adding new nonterminals
    @staticmethod
    def _add_new_rules(new_rules: RulesMap,
                       initial_rules: RulesMap) -> RulesMap:
        '''
        Params
        - `new_rules`: collection of new rules to insert, keyed by nonterminal
        - `rules`: rules map to add rules to

        Overview
        Merge new_rules into initial_rules and return new rules dict
        - head of all new rules MUST be an existing nonterminal
        - adding duplicate rules is fine as they are ignored
        - lenlex order of bodies is preserved
        - NOTE no new symbols can be introduced
            - use _add_new_nonterminals() for rules headed by new nonterminal

        Return
        - new rules map that is the union of rules from new_rules and initial_rules
        '''
        # Don't modify original rules map
        rules_return = initial_rules.copy()

        # Check all nonterminals already exist
        if any(nonterminal not in initial_rules for nonterminal in new_rules):
            raise ValueError('Cannot add rules for nonterminals not already present in rules map.')
        
        # TODO check symbols in rule bodies to prevent collisions?

        # Update bodies for each nonterminal
        for nonterminal in new_rules:
            # Merged tuple of initial and new rules, without duplicates, sorted by lenlex
            updated = tuple(sorted(set(initial_rules[nonterminal]) | set(new_rules[nonterminal]), 
                                   key=lambda body: (len(body), body)))
            # Update bodies in final rules map
            rules_return[nonterminal] = updated

        return rules_return
    
    # Add new nonterminals (and corresponding rules) to existing rules map
    # NOTE cannot be used to add rules for existing nonterminals
    @staticmethod
    def _add_new_nonterminals(new_rules: RulesMap,
                              initial_rules: RulesMap) -> RulesMap:
        '''
        Params
        - `new_rules`: collection of rules for new nonterminals to add
        - `initial_rules`: rules map to merge additions into

        Overview
        Add collection of new nonterminals and their respective rules to existing rules map, return new rules map
        - head of all new rules MUST be a new nonterminal
        - bodies of new rules can contain existing terminals, existing nonterminals, new nonterminals, and nothing else
            - in particular, new terminals NOT allowed
        - no duplicates and lenlex order of bodies is assumed of new_rules (TODO enforce this?)
        - NOTE adding new rules for existing nonterminals is NOT allowed
            - this is done via _add_new_rules()

        Implementation
        - ensure new nonterminals don't collide with any existing symbols
        - ensure all symbols in new_rules are either existing terminals, existing nonterminals, or new nonterminals
        - merge new_rules into initial_rules by defining keys (guaranteed new keys by above)
        - return new rules map

        Return
        - new rules map
        '''
        rules_return = initial_rules.copy() # Don't modify intial_rules

        existing_nonterminals, existing_terminals = CFG._extract(initial_rules)
        new_nonterminals, new_terminals = CFG._extract(new_rules)

        # Check new nonterminal collisions
        for nonterminal in new_nonterminals:
            if nonterminal in existing_nonterminals or nonterminal in existing_terminals:
                raise ValueError(f'Cannot add new nonterminal \'{nonterminal}\' as it collides with an existing symbol.')
        
        # Check no new terminals
        # New symbols that are not new nonterminals must either be existing terminals or existing nonterminals
        for new_symbol in new_terminals:
            if new_symbol not in existing_terminals and new_symbol not in existing_nonterminals:
                raise ValueError(f'Unrecognised symbol \'{new_symbol}\' in new rule body.')
            
        # Merge new nonterminals into return dict
        for head, bodies in new_rules.items():
            rules_return[head] = bodies
        return rules_return

    
    # Return tuple of bodies with all combinations of occurrences of target symbol removed from given body
    @staticmethod
    def _remove_occurrences_of(target: str,
                               body: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
        '''
        Params
        - `target`: symbol whose occurrences are to be removed
        - `body`: rule body to remove occurrences from

        Overview
        Returns tuple of new rule bodies, where each body has a subset of occurences of target removed
        - e.g. for target 'A' and body 'uAv', return {'uv'}
        - e.g. for target 'A' and body 'uAvAw', return {'uvAw', 'uAvw', 'uvw'}
        - does not include original body with no occurrences removed
        - returned bodies are in lenlex order
        - NOTE this method is not called when body only consists of target symbol

        Implementation
        - generate `positions` list of all indices that contain target in body
        - for all subsets of positions (excl empty subset):
            - yield a new rule body equal to `body` except with all indices in the subset removed
        - return all yielded new rule bodies

        Return
        - tuple of bodies with occurences of target removed
        '''
        # Initialise collection of return rule bodies with target omitted
        bodies_return = []

        # All occurrences of target in body
        positions = [i for i, symbol in enumerate(body) if symbol == target]

        # Helper to generate all subsets of positions via recursion
        # NOTE order doesn't matter since the final rules are sorted anyway (but should be implicitly ordered anyway)
        def all_subsets(items: list[int]) -> Generator[list[int]]:
            # Base case
            if not items:
                yield []
            # Recursive case:
            # Take all subsets of remaining list after first element, and either include or exclude first element
            else:
                for subset in all_subsets(items[1:]):
                    yield subset
                    yield [items[0]] + subset
        
        # For each non-empty subset, add new body that omits subset indices
        for subset in all_subsets(positions):
            # Exclude empty subset
            if not subset: continue

            bodies_return.append(tuple(symbol for i, symbol in enumerate(body) if i not in subset))

        # Sort new bodies by lenlex and convert to tuple
        bodies_return = tuple(sorted(bodies_return, key=lambda rule: (len(rule), rule)))
        return bodies_return

    # Return rules map with bad ε-rules removed
    @staticmethod
    def remove_bad_epsilon_rules(rules: RulesMap,
                                 start: str) -> RulesMap:
        '''
        Params
        - `rules`: rules map to remove bad ε-rules from
        - `start`: CFG start nonterminal

        Overview
        Construct new rules map with no bad ε-rules, while preserving the generated language
        - doesn't modify intial rules map

        Implementation
        Use the standard bad ε-rules process:
        - for all bad ε-rules 'A -> ε':
            - remove the bad ε-rule and record its removal
            - for all rules containing 'A' in their body:
                - add a collection of new rules with the same head, and bodies that omit each occurrence of 'A'
                    - e.g. for 'B -> uAv' add 'B -> uv'
                    - e.g. for 'B -> uAvAw' add 'B -> uvAw', 'B -> uAvw', 'B -> uvw'
                    - for special case 'B -> A', add 'B -> ε' UNLESS it was already removed
                        - NOTE this can add new bad e-rules to remove later
        - repeat above until no bad ε-rules remain

        Return
        - new rules map with no bad e-rules
        '''
        # Don't modify rules in-place
        rules_return = rules.copy()

        # Initialise list of bad ε-rules to remove
        to_remove = [] # List of nonterminals 'A' which have a rule 'A -> ε' 
        for head, bodies in rules_return.items():
            if any(body == ('',) for body in bodies) and head != start:
                to_remove.append(head)

        # Initialise set of removed bad ε-rules, so they are not re-added
        # NOTE only need to index by nonterminal head, since body ' -> ε' is implied
        removed = set()

        # Iteratively remove bad ε-rules until none remaining
        while to_remove:
            # Choose next bad ε-rule
            nonterminal = to_remove.pop(0)
            
            # Remove original bad ε-rule from nonterminal's bodies
            rules_return[nonterminal] = CFG._delete_body_from_bodies(('',), rules_return[nonterminal])
            removed.add(nonterminal)

            # Add new rules with `nonterminal` omitted
            
            # Determine all rules which have an occurrence of `nonterminal`
            # Maps nonterminals to its respective rules containing `nonterminal`
            rules_to_add_from = CFG._get_bodies_containing(nonterminal, rules_return)

            # Initialise collection of rules to replace the rule just removed
            # Maps nonterminals to their respective new rules with `nonterminal` omitted
            rules_replacement = {}
            
            # For each body, generate new bodies with nonterminal omitted
            for head, bodies in rules_to_add_from.items():
                for body in bodies:

                    # Case unit rule
                    if body == (nonterminal,):
                        # Only add new e-rule if not already removed
                        if head not in removed:
                            _append_dict_value(head, ('',), rules_replacement)
                            # If not the start nonterminal, schedule new ε-rule for removal in later iteration
                            # and ensure no duplicates in worklist
                            if head != start and head not in to_remove:
                                to_remove.append(head)

                    # Case compound rule
                    else:
                        # Generate new rules with each occurrence of nonterminal omitted, and schedule them to add
                        new_bodies = CFG._remove_occurrences_of(nonterminal, body)
                        for new_body in new_bodies:
                            _append_dict_value(head, new_body, rules_replacement)

            # Convert new rule bodies from lists to tuples before adding
            rules_replacement = {head: tuple(bodies) for head, bodies in rules_replacement.items()}
            # Add new rules with nonterminal omitted (NOTE duplicates ignored and lenlex order preserved)
            rules_return = CFG._add_new_rules(rules_replacement, rules_return)

        return rules_return

    # Return rules map with unit rules 'A -> B' removed
    @staticmethod
    def remove_unit_rules(rules: RulesMap) -> RulesMap:
        '''
        Params
        - `rules`: rules map to remove unit rules from

        Overview
        Construct new rules map with no unit rules
        - doesn't modify initial rules map
        - NOTE assumes no bad epsilon rules present

        Implementation
        Use the standard unit rule removal process:
        - for all unit rules 'A -> B':
            - remove 'A -> B'
            - for all rules 'B -> body' 
                - add rule 'A -> body', UNLESS it is a previously removed unit rule
                    - NOTE this can add a new unit rule to remove later
        - repeat above until no unit rules remain

        Return
        - new rules map with no unit rules
        '''
        # Don't modify rules in-place
        rules_return = rules.copy()

        # Determine symbols to distinguish between unit rule and single terminal production
        nonterminals, terminals = CFG._extract(rules_return)

        # Initialise unit rules to remove
        to_remove = [] # List of all tuples ('A', 'B') such that 'A -> B' is a unit rule
        for head, bodies in rules_return.items():
            for body in bodies:
                # Unit rule if only one symbol, which is a nonterminal
                if len(body) == 1 and body[0] in nonterminals:
                    to_remove.append((head, body[0]))
        
        # Track removed unit rules so they are not re-added
        removed = set() # Pairs ('A', 'B') where 'A -> B' already removed

        # Remove unit rules until none remaining
        while to_remove:
            # Choose next rule 'A -> B'
            nonterminal_head, nonterminal_body = to_remove.pop(0)

            # Remove rule
            rules_return[nonterminal_head] = CFG._delete_body_from_bodies((nonterminal_body,), rules_return[nonterminal_head])
            removed.add((nonterminal_head, nonterminal_body))

            # Initialise replacement rules 'A -> body' to add
            # Maps nonterminal head to bodies to add
            # NOTE there should only be one key, namely 'nonterminal_head'
            rules_replacement = {}

            # For all rules 'B -> body', add rule 'A -> body' if not previously removed unit rule
            for body in (body for body in rules_return[nonterminal_body]):

                if len(body) == 1:

                    # Case body is a nonterminal and 'A -> body' already removed - don't add
                    if (nonterminal_head, body[0]) in removed:
                        continue

                    # Case body is a terminal - add
                    elif body[0] in terminals:
                        _append_dict_value(nonterminal_head, body, rules_replacement)

                    # Case body is a nonterminal and 'A -> body' not already removed - add and schedule for later removal
                    else:
                        _append_dict_value(nonterminal_head, body, rules_replacement)
                        # Ensure no duplicates in removal workload
                        if (nonterminal_head, body[0]) not in to_remove:
                            to_remove.append((nonterminal_head, body[0]))

                # Case 'A -> body' is a compound rule - always add
                else:
                    _append_dict_value(nonterminal_head, body, rules_replacement)

            # Convert new rule bodies from lists to tuples before adding
            rules_replacement = {head: tuple(bodies) for head, bodies in rules_replacement.items()}
            # Add new rules (NOTE duplicates ignored and lenlex order preserved)
            rules_return = CFG._add_new_rules(rules_replacement, rules_return)
            
        return rules_return
    
    # Return rules map with all rules of body length greater than 2 removed
    @staticmethod
    def remove_rules_body_length_greater_than_2(rules: RulesMap) -> RulesMap:
        '''
        Params
        - `rules`: rules map to remove rules from

        Overview
        Construct new rules map with no rules whose body has length >2
        - doesn't modify initial rules map
        - NOTE assumes no bad epsilon rules and no unit rules

        Implementation
        - for all rules 'A -> a1 a2 ... an' where n > 2:
            - remove original rule
            - introduce n - 2 new nonterminals 'A1', 'A2', ..., 'A{n-2}'
                - index them by rule number to ensure they are unique to specific rule
            - add n - 1 new rules 'A -> a1 A1', 'A1 -> a2 A2', ..., 'A{n-2} -> a{n-1} an'
        - return new rules map 

        Return
        - new rules map with no rule bodies of length >2
        '''
        # Don't modify rules in-place
        rules_return = rules.copy()

        # All rules to remove
        to_remove = CFG._get_bodies_length_greater_than(2, rules_return)

        # Iteratively remove all rules
        for head, bodies in to_remove.items():
            for i, body in enumerate(bodies):
                # Store body length
                length = len(body)

                # Remove original rule 'A -> a1 a2 ... an'
                rules_return[head] = CFG._delete_body_from_bodies(body, rules_return[head])

                # Initialise replacement rules to add
                # NOTE does NOT include first new rule 'A -> a1 A1', since headed by existing nonterminal
                rules_replacement = {} # TODO could probably go outside loop in this method, since to_remove never grows

                # Introduce `length - 2` new nonterminals
                new_nonterminals = CFG._new_nonterminals_chomsky_chain(head,
                                                                       i,
                                                                       length - 2)

                # Introduce corresponding `length - 1` new rules
                # 'A -> a1 A1', 'A1 -> a2 A2', ..., 'An-2 -> an-1 an'
                for j in range(length - 1):

                    # Create each new rule body
                     
                    # Final rule - both symbols nonterminals
                    if j == length - 2:
                        new_body = (body[j], body[j + 1])
                    # Non-final rule - first symbol new terminal
                    else:
                        new_body = (body[j], new_nonterminals[j])

                    # Add new rules

                    # First rule headed by existing nonterminal
                    if j == 0:
                        rules_return = CFG._add_new_rules({head: (new_body,)}, rules_return)
                    else:
                        rules_replacement[new_nonterminals[j - 1]] = (new_body,)

                # Add remaining new rules
                rules_return = CFG._add_new_nonterminals(rules_replacement, rules_return)

        return rules_return





    
    
    

    # Decide if CFG is in Chomsky Normal Form
    @staticmethod
    def _is_chomsky_normal_form(rules: RulesMap,
                                start: str) -> bool:
        '''
        Params
        - `rules`: rules map to test
        - `start`: CFG start nonterminal

        Overview
        Determine if given rules map is in Chomsky normal form,
        that is, every rule must be of one of these forms:
            1. 'A -> BC' where all are nonterminals, and 'B' and 'C' cannot be the start nonterminal
            2. 'A -> a' where A is a nonterminal and 'a' is a terminal
            3. 'S -> ε' where S must be the start nonterminal
        
        Return
        - True if in Chomsky normal form, False otherwise
        '''
        # Check start is valid
        if start not in rules:
            raise ValueError(f'Invalid start nonterminal \'{start}\'')

        # Get symbol sets, (TODO maybe refactor into method params?)
        nonterminals, terminals = CFG._extract(rules)

        for head, bodies in rules.items():
            for body in bodies:
                # Form 1
                if len(body) == 2:
                    if not all(symbol in nonterminals for symbol in body):
                        return False
                    if any(symbol == start for symbol in body):
                        return False
                # Forms 2 and 3
                elif len(body) == 1:
                    # Form 3
                    if body == ('',):
                        if head != start:
                            return False
                    # Form 2
                    else:
                        if body[0] not in terminals:
                            return False
                # Length >2 - can't match any form
                else:
                    return False
        return True

    # Convert grammar to Chomsky normal form
    def to_chomsky_normal_form(self) -> 'CFG':
        '''
        Returns a *new* CFG in chomsky normal form via the canonical process:
        - add `new_start` nonterminal and rule 'new_start -> start'
            - name of new_start must be distinct from all symbols in original CFG
        - remove all bad ε-rules
        - remove all unit rules
        - convert remaining rules to correct form
        '''
        # Generate distinct new start symbol and initial rule
        new_start = disjoint_symbol('S', set(self.nonterminals) | set(self.terminals))
        

        
    
        # Sketch outline
        new_rules = CFG.remove_bad_epsilon_rules(self.rules, self.nonterminals, self.start)
        new_rules = CFG.remove_unit_rules(new_rules, self.nonterminals, self.start)
        new_rules = CFG.convert_proper_form(new_rules, self.nonterminals, self.start)
        # Rule to yield initial start from new start
        new_rules[new_start] = ((self.start,),)

        raise NotImplementedError
        
        return CFG(new_rules, new_start)





    