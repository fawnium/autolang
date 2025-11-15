from autolang.backend.utils import disjoint_symbol, _append_dict_value
from autolang.visuals.utils_visuals import eps

from collections.abc import Iterable, Container, Generator, Sequence

'''
Context-Free Grammar Class

NOTE naming conventions
symbol: any string appearning in CFG, i.e. a letter
nonterminal: symbol that is the head of a rule, i.e. variable
terminal: symbol that is not a nonterminal, i.e. appears in final derived word
subsitution/sub: sequence of symbols that a nonterminal can be replaced by, i.e. body of single rule
substitutions: list of all rule bodies for given nonterminal 

'''

class CFG:

    def __init__(self,
                 rules: dict[str, Iterable[Iterable[str] | str]],
                 start: str):
        '''
        - `rules`: maps nonterminals to collection of substitutions
            - each substitution is either a single string (unit rule) or collection of strings (each string is ONE symbol)
        - `start`: start nonterminal, must be included in rules
        '''
        # Convert rules to standard form
        self.rules = CFG._canonise_rules(rules)
        
        # Check start is listed as a nonterminal
        if start not in rules:
            raise ValueError(f'Start symbol \'{start}\' must be listed in rules.')
        self.start = start

        # Extract symbol sets
        self.nonterminals, self.terminals = CFG._extract(self.rules)
        
    # Ensure rules dict is correctly formatted and convert containers to tuples for consistency
    @staticmethod
    def _canonise_rules(rules: dict[str, Iterable[Sequence[str] | str]]) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - iterate through each str: Iterable pair in rules dict
            - NOTE empty string '' disallowed as a nonterminal
            - NOTE strings NOT allowed as dict values, even though they are iterable
        - the parent Iterable is a list of substitutions (i.e. rule bodies) for the given nonterminal str
            - NOTE empty iterable IS allowed even though it means nonterminal can't yield anything
        - elements of the parent iterable can either be literal strings (unit rule), or collection of strings (compound rule)
            - NOTE a literal string is interpreted as a single symbol, NOT a concatenation of multiple symbols
            - NOTE a collection of strings must be ordered to preserve rule semantics
        - for each element in parent Iterable:
            - if it is a string, wrap in tuple and add to canonical substitutions
            - if it is an sequence and NOT a string:
                - if empty, interpret as e-rule
                    - NOTE the correct e-rule syntax is tuple('') NOT tuple(), but users may expect the latter
                - ensure no '' symbol if compound rule
                    - e.g. " A -> 'u','','v' " - '' adds nothing and could cause unexpected behaviour
                - convert to tuple and add to canonical substitutions
        - for each nonterminal:
            - deduplicate canonical substitutions (repeated rules are redundant)
            - sort in lenlex order
            - convert to tuple
            - assign to final dict entry
        '''
        if not isinstance(rules, dict):
            raise TypeError('CFG rules must be a dict mapping nonterminals to rules.')

        canonical = {} # Initialise canonical dict
        for nonterminal, substitutions in rules.items():

            if not isinstance(nonterminal, str):
                raise TypeError(f'Nonterminal \'{nonterminal}\' must be a string.')
            # '' Cannot be a nonterminal
            if not nonterminal:
                raise ValueError('Empty string \'\' not allowed as a nonterminal.')

            if not isinstance(substitutions, Iterable):
                raise TypeError(f'Substitutions for nonterminal \'{nonterminal}\' must be iterable.')
            # String as value not allowed (TODO allow if unambiguous?)
            if isinstance(substitutions, str):
                raise TypeError(f'Rule body \'{substitutions}\' must be inside an iterable.')
            
            canonical_subs = [] # Substitutions to be converted, final type will be tuple[tuple[str, ...]]

            for sub in substitutions:
                if isinstance(sub, str):
                    # NOTE using tuple() directly would separate chars into individual entries, which is not intended
                    canonical_subs.append((sub,))

                # NOTE in this case `sub` will NOT be a string, since that is caught in above case
                elif isinstance(sub, Sequence):
                    # Ensure all strings
                    if not all(isinstance(symbol, str) for symbol in sub):
                        raise TypeError('All terminals and nonterminals must be strings.')
                    
                    # Convert empty sub to ('',)
                    if len(sub) == 0:
                        sub = ('',)
                    
                    # Ensure no '' in compound rule
                    if len(sub) > 1 and '' in sub:
                        raise ValueError(f'Empty symbol \'\' not allowed in non-unit rule.')

                    canonical_subs.append(tuple(sub))

                else:
                    raise TypeError(f'Rule body \'{sub}\' must be an ordered collection of strings.')
                
            # Remove duplicate subs, sort by lenlex, convert to tuple
            canonical[nonterminal] = tuple(sorted(set(canonical_subs), key=lambda sub: (len(sub), sub)))
        return canonical

    # Establish terminals and nonterminals from rules
    @staticmethod
    def _extract(rules: dict[str, tuple[tuple[str, ...], ...]]) -> tuple[tuple[str, ...], tuple[str, ...]]:
        '''
        - initialise terminals and nonterminals as sets
        - iterate through rules
            - add each nonterminal (i.e. rule key) to nonterminals
            - for each substition in each nonterminal's list of substitutions, add all symbols in the substitution to terminals
                - NOTE nonterminals can yield other nonterminals, so these will be filtered out
        - filter out nonterminals from `terminals` to leave only true terminals
        - sort and convert to tuples for return

        Return: (`nonterminals`, `terminals`)
        '''
        terminals = set()
        nonterminals = set()

        # Extract symbols from rules dict
        for nonterminal, substitutions in rules.items():
            nonterminals.add(nonterminal)
            for sub in substitutions:
                for symbol in sub:
                    terminals.add(symbol)

        # Filter nonterminals and empty symbol '' out of `terminals`
        terminals = {symbol for symbol in terminals if symbol not in nonterminals and symbol}

        # Sort symbols and convert to tuple
        # TODO make these sets?
        nonterminals = tuple(sorted(nonterminals))
        terminals = tuple(sorted(terminals))
        return nonterminals, terminals
    
    def __repr__(self):
        repr_str = 'CFG(\n'
        # Iterate such that start nonterminal appears first
        for nonterminal, substitutions in ((self.start, self.rules[self.start]),) + tuple(item 
                                                                                          for item in self.rules.items() 
                                                                                          if item[0] != self.start):
            repr_str += nonterminal + ' ::= '
            repr_str += ' | '.join(' '.join(eps(symbol) for symbol in substitution) for substitution in substitutions)
            repr_str += '\n'
        repr_str += ')'
        return repr_str
    
    def __str__(self):
        return 'CFG with nonterminals {' + ','.join(self.nonterminals) + '} and terminals {' + ','.join(self.terminals) + '}'
    
    # UNION METHODS
    
    # Rename symbols in CFG
    # TODO better collision checking
    @staticmethod
    def _rename_symbols(cfg: 'CFG', rename_map: dict[str, str]) -> 'CFG':
        '''
        - `rename_map`: keys are current nonterminals, values are the corresponding renamed nonterminals
        
        Change every symbol instance in rules to its image under rename_map
        - this applies to both keys and instances within substitutions
        - NOTE this function can be used to rename terminals for generality, but is only intended for nonterminals
        - if a symbol does not have an image in rename_map, it stays the same
        '''
        # Ensure no collision between renamed nonterminals and existing terminals
        if any(symbol in cfg.terminals for symbol in rename_map.values()):
            raise ValueError('Renamed nonterminal collides with existing terminal.')

        new_rules = {}
        
        for nonterminal, substitutions in cfg.rules.items():
            new_subs = []
            for sub in substitutions:
                # Rename each symbol in substitution, add to list of renamed substitutions
                # Default to original name
                new_subs.append(tuple(rename_map.get(symbol, symbol) for symbol in sub))
            new_rules[rename_map.get(nonterminal, nonterminal)] = tuple(new_subs)

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
        new_rules = {nonterminal: substitutions for nonterminal, substitutions in renamed_self.rules.items()}
        for nonterminal, substitutions in renamed_other.rules.items():
            new_rules[nonterminal] = substitutions

        # Add start rule
        new_rules[new_start] = ((renamed_self.start,), (renamed_other.start,))

        return CFG(new_rules, new_start)
    
    # CHOMSKY NORMAL FORM METHODS

    # Return new tuple of substitutions with given `target` removed
    @staticmethod
    def _delete_sub_from_substitutions(target: tuple[str, ...], 
                                       substitutions: tuple[tuple[str, ...], ...]) -> tuple[tuple[str, ...], ...]:
        if target not in substitutions:
            raise ValueError(f'Substitution \'{target}\' not present in tuple, cannot delete.')

        return tuple(sub for sub in substitutions if sub != target)

    # Return all rules that contain given nonterminal in body
    @staticmethod
    def _get_rules_containing(target: str,
                              rules: dict[str, tuple[tuple[str, ...], ...]]) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - `target`: symbol to query presence of within substitutions
        - `rules`: map of rules to query

        Returns dict mapping nonterminals to ONLY its substitutions containing given `target` nonterminal
        - if a nonterminal has no rules containing target, then it does not have a key in dict
        '''
        # Check target is a valid nonterminal
        if target not in rules:
            raise ValueError(f'Symbol \'{target}\' must be a nonterminal.')
        # Return object
        filtered_rules = {}

        for nonterminal, substitutions in rules.items():
            for sub in substitutions:
                # Check if nonterminal contained in rule body
                if target in sub:
                    # Update list of rules for nonterminal, adding key if none already
                    _append_dict_value(nonterminal, sub, filtered_rules)
        
        # Convert lists to tuples for return
        return {nonterminal: tuple(substitutions) for nonterminal, substitutions in filtered_rules.items()}
    
    # Insert new collection of rules to existing rules map
    # NOTE ONLY for adding new rules for existing nonterminals, NOT for adding new nonterminals
    @staticmethod
    def _add_new_rules(new_rules: dict[str, tuple[tuple[str, ...], ...]],
                       initial_rules: dict[str, tuple[tuple[str, ...], ...]]) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - `new rules`: collection of new rules to insert, keyed by nonterminal
        - `rules`: rules map to add rules to

        Return updated rules map that is the same as `rules`, but with additional rules for specified nonterminals
        - NOTE only intended for no new symbols being introduced (terminals OR nonterminals)

        '''
        # Don't modify original rules map
        rules_return = initial_rules.copy()

        # Check all nonterminals already exist
        if any(nonterminal not in initial_rules for nonterminal in new_rules):
            raise ValueError('Cannot add rules for nonterminals not already present in rules map.')

        # Update substitutions for each nonterminal
        for nonterminal in new_rules:
            # Merged tuple of initial and new rules, without duplicates, sort by lenlex
            updated = tuple(sorted(set(initial_rules[nonterminal]) | set(new_rules[nonterminal]), 
                                   key=lambda rule: (len(rule), rule)))
            # Update substitutions in final rules map
            rules_return[nonterminal] = updated

        return rules_return
    
    # Add new nonterminal (and corresponding rules) to existing rules map
    # NOTE cannot be used to add rules for existing nonterminals
    @staticmethod
    def _add_new_nonterminals(new_rules: dict[str, tuple[tuple[str, ...], ...]],
                              initial_rules: dict[str, tuple[tuple[str, ...], ...]]) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - `new_rules`: collection of new rules, mapping new nonterminals to their respective substitutions
            - NOTE must be keyed only by NEW nonterminals
        - `initial_rules`: rules map to merge additions into
        - `start`: start terminal of initial CFG

        Implementation:
        - ensure new nonterminals (i.e. new_rules keys) don't collide with any existing symbols
        - ensure all symbols in new_rules are either: existing terminals, existing nonterminals, or new nonterminals
            - NOTE in particular, new terminals NOT allowed
        - merge new_rules into initial_rules by defining keys (guaranteed new keys by above)
        '''
        existing_nonterminals, existing_terminals = CFG._extract(initial_rules)
        new_nonterminals, new_terminals = CFG._extract(new_rules)

        # Check new nonterminal collisions
        for nonterminal in new_nonterminals:
            if nonterminal in existing_nonterminals or nonterminal in existing_terminals:
                raise ValueError(f'Cannot add new nonterminal \'{nonterminal}\' as it collides with an existing symbol.')
            
        # Check no other new symbols
        # NOTE suffices to check *terminals* in new_rules, as new nonterminals are allowed
        # 'new terminals' should either be existing terminals or existing nonterminals (new nonterminals already filtered out)
        for new_symbol in new_terminals:
            if new_symbol not in existing_terminals and new_symbol not in existing_nonterminals:
                raise ValueError(f'Unrecognised symbol \'{new_symbol}\' in new rule body.')
            
        # Merge into return dict
        rules_return = initial_rules.copy()
        for new_nonterminal, substitutions in new_rules.items():
            rules_return[new_nonterminal] = substitutions

        return rules_return

    
    # Return list of new rules with each occurrence of given nonterminal removed
    @staticmethod
    def _remove_occurrences_of(target: str,
                              sub: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
        '''
        - `target`: nonterminal whose occurrences are to be removed
        - `sub`: rule body to remove occurrences from

        Returns tuple of new rule bodies with each occurrence of target removed
        - e.g. for target 'A' and sub 'uAv', return {'uv'}
        - e.g. for target 'A' and sub 'uAvAw', return {'uvAw', 'uAvw', 'uvw'}

        NOTE this function is NOT called when sub only consists of 'target'

        Implementation:
        - generate `positions` list of all indices that contain `target` in `sub`
        - for all subsets of `positions` (EXCL empty subset):
            - yield a new rule body equal to `sub` except with all indices in the subset removed
        - return all yielded new rule bodies
        '''
        # Initialise collection of return rule bodies with target omitted
        rules_return = []

        # All occurrences of target in sub
        positions = [i for i, symbol in enumerate(sub) if symbol == target]

        # Helper to generate all subsets of `positions` via recursion
        # NOTE order doesn't matter since the final rules are sorted anyway
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
        
        # For each non-empty subset, add new rule that omits subset indices
        for subset in all_subsets(positions):
            # Exclude empty subset - it corresponds to the input `sub`
            if not subset: continue

            rules_return.append(tuple(symbol for i, symbol in enumerate(sub) if i not in subset))

        # Sort new rules by len-lex and convert to tuple
        rules_return = tuple(sorted(rules_return, key=lambda rule: (len(rule), rule)))
        return rules_return

    
    # Return rules mapping with bad ε-rules removed
    @staticmethod
    def remove_bad_epsilon_rules(rules: dict[str, tuple[tuple[str, ...], ...]],
                                 start: str) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - `rules`: rules map to remove bad ε-rules from
        - `start`: CFG start nonterminal

        Construct a new rules map with no bad ε-rules, that generates the same language as `rules`.
        Use the standard bad ε-rules process:
        - for all bad ε-rules 'A -> ε':
            - remove the bad ε-rule and record its removal
            - for all rules containing 'A' in their body:
                - add a collection of new rules with the same head, and bodies that omit each occurrence of 'A'
                    - e.g. for 'B -> uAv' add 'B -> uv'
                    - e.g. for 'B -> uAvAw' add 'B -> uvAw', 'B -> uAvw', 'B -> uvw'
                    - for special case 'B -> A', add 'B -> ε' UNLESS it was already removed
        - repeat above until no bad ε-rules remain
        '''
        # Don't modify rules in-place
        rules_return = rules.copy()

        # Initialise list of bad ε-rules to remove
        to_remove = [] # List of nonterminals 'A' which have a rule 'A -> ε' 
        for nonterminal, substitutions in rules_return.items():
            if any(sub == ('',) for sub in substitutions) and nonterminal != start:
                to_remove.append(nonterminal)

        # Initialise set of removed bad ε-rules, so they are not re-added
        # NOTE only need to index by nonterminal, since body ' -> ε' is implied
        removed = set()

        # Iteratively remove bad ε-rules until none remaining
        while to_remove:
            # Choose next bad ε-rule
            nonterminal = to_remove.pop(0)
            
            # Remove original bad ε-rule from nonterminal's substitutions
            rules_return[nonterminal] = CFG._delete_sub_from_substitutions(('',), rules_return[nonterminal])
            removed.add(nonterminal)

            # Add new rules with `nonterminal` omitted
            
            # Determine all rules which have an occurrence of `nonterminal`
            # Maps nonterminals to its respective rules containing `nonterminal`
            rules_to_add_from = CFG._get_rules_containing(nonterminal, rules_return)

            # Initialise collection of rules to replace the rule just removed
            # Maps nonterminals to their respective new rules with `nonterminal` omitted
            rules_replacement = {}
            
            # For each rule, generate new rules with nonterminal omitted
            for head, substitutions in rules_to_add_from.items():
                for sub in substitutions:

                    # Edge case for rule 'head -> nonterminal'
                    if sub == (nonterminal,):
                        # Only add new e-rule if not already removed
                        if head not in removed:
                            _append_dict_value(head, ('',), rules_replacement)
                            # If not the start nonterminal, schedule new ε-rule for removal in later iteration
                            # and ensure no duplicates in worklist
                            if head != start and head not in to_remove:
                                to_remove.append(head)

                    # Case for NOT 'head -> nonterminal'
                    else:
                        # Generate new rules with each occurrence of nonterminal omitted, and schedule them to add
                        new_rules = CFG._remove_occurrences_of(nonterminal, sub)
                        for new_rule in new_rules:
                            _append_dict_value(head, new_rule, rules_replacement)

            # Convert list of new rules to tuple before adding
            rules_replacement = {key: tuple(val) for key, val in rules_replacement.items()}
            # Add new rules with nonterminal omitted (NOTE duplicates are ignored)
            rules_return = CFG._add_new_rules(rules_replacement, rules_return)

        return rules_return

    # Return rules mapping with unit rules 'A -> B' removed
    @staticmethod
    def remove_unit_rules(rules: dict[str, tuple[tuple[str, ...], ...]],
                          ) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - `rules`: rules map to remove unit rules from

        # NOTE assumes no epsilon rules present

        - for all rules 'A -> B':
            - remove 'A -> B'
            - for all rules 'B -> u' (NOTE 'u' is an arbitrary-length rule body):
                - add rule 'A -> u', unless it is a previously removed unit rule
        - repeat above until no unit rules remain
        '''
        # Don't modify rules in-place
        rules_return = rules.copy()

        nonterminals, terminals = CFG._extract(rules_return)

        # Initialise unit rules to remove
        to_remove = [] # List of all tuples ('A', 'B') such that 'A -> B' is a rule
        for nonterminal, substitutions in rules_return.items():
            for sub in substitutions:
                # Unit rule if only one symbol, which is a nonterminal
                if len(sub) == 1 and sub[0] in nonterminals:
                    to_remove.append((nonterminal, sub[0]))
        
        # Track removed unit rules so they are not re-added
        removed = set() # Pairs ('A', 'B') where 'A -> B' already removed

        # Remove unit rules until none remaining
        while to_remove:
            # Choose next rule 'A -> B'
            nonterminal_head, nonterminal_body = to_remove.pop(0)

            # Remove rule
            rules_return[nonterminal_head] = CFG._delete_sub_from_substitutions((nonterminal_body,), rules_return[nonterminal_head])
            removed.add((nonterminal_head, nonterminal_body))

            # Initialise replacement rules to add, i.e. 'A -> u'
            # Maps nonterminal head to bodies to add
            # NOTE in this case should only be one key, namely 'nonterminal_head'
            rules_replacement = {}

            # For all rules 'B -> u', add rule 'A -> u' if not previously removed unit rule
            for sub in (sub for sub in rules_return[nonterminal_body]):

                # Case 'A -> u' is a unit rule
                if len(sub) == 1:

                    # Case 'u' is a nonterminal and 'A -> u' already removed - don't add
                    if (nonterminal_head, sub[0]) in removed:
                        continue

                    # Case 'u' is a terminal - add
                    elif sub[0] in terminals:
                        _append_dict_value(nonterminal_head, sub, rules_replacement)

                    # Case 'u' is a nonterminal and 'A -> u' not already removed - add and schedule for later removal
                    else:
                        _append_dict_value(nonterminal_head, sub, rules_replacement)
                        # Ensure no duplicates in removal workload
                        if (nonterminal_head, sub[0]) not in to_remove:
                            to_remove.append((nonterminal_head, sub[0]))

                # Case 'A -> u' is a compound rule - always add
                else:
                    _append_dict_value(nonterminal_head, sub, rules_replacement)

            # Convert list of new rules to tuple before adding
            rules_replacement = {key: tuple(val) for key, val in rules_replacement.items()}
            rules_return = CFG._add_new_rules(rules_replacement, rules_return)
            
        return rules_return
    
    
    # Return rules with all bodies converted to normal form by introducting new nonterminals
    @staticmethod
    def convert_proper_form(rules: dict[str, tuple[tuple[str, ...], ...]],
                            start: str) -> dict[str, tuple[tuple[str, ...], ...]]:
        raise NotImplementedError
    

    # Decide if CFG is in Chomsky Normal Form
    @staticmethod
    def _is_chomsky_normal_form(rules: dict[str, tuple[tuple[str, ...], ...]],
                               start: str) -> bool:
        '''
         - for each rule, check if it is of one of these forms:
            1. 'A -> BC' where all are nonterminals, and 'B' and 'C' cannot be the start terminal
            2. 'A -> a' where A is a nonterminal and 'a' is a terminal
            3. 'S -> ε' where S must be the start nonterminal
        - if any rule fails the above, return False, else return True
        '''
        # Get symbol sets, (TODO maybe refactor into method args?)
        nonterminals, terminals = CFG._extract(rules)

        for nonterminal, substitutions in rules.items():
            for sub in substitutions:
                # Form 1
                if len(sub) == 2:
                    if not all(symbol in nonterminals for symbol in sub):
                        return False
                    if any(symbol == start for symbol in sub):
                        return False
                # Forms 2 and 3
                elif len(sub) == 1:
                    # Form 3
                    if sub == ('',):
                        if nonterminal != start:
                            return False
                    # Form 2
                    else:
                        if sub[0] not in terminals:
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





    