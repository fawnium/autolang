from autolang.backend.utils import disjoint_symbol, _append_dict_value
from autolang.visuals.utils_visuals import eps

from collections.abc import Iterable, Container

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
        self.rules = self._canonise_rules(rules)
        
        # Check start is listed as a nonterminal
        if start not in rules:
            raise ValueError(f'Start symbol \'{start}\' must be listed in rules.')
        self.start = start

        # Extract symbol sets
        self.nonterminals, self.terminals = self._extract()

    # Ensure rules dict is correctly formatted and convert containers to tuples for consistency
    def _canonise_rules(self, rules: dict[str, Iterable[Iterable[str] | str]]) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - iterate through each str: Iterable pair in rules dict
        - the parent Iterable is a list of substitutions for the given nonterminal str
        - elements of the parent iterable can either be literal strings, or collections of strings
            - NOTE a literal string is interpreted as a single symbol, NOT a concatenation of multiple symbols
        - for each element in parent Iterable:
            - if it is a string, wrap in tuple and add to canonical substitutions
                - This is a unit rule case
            - if it is an iterable and NOT a string, convert to tuple and add to canonical
                - This is a non-unit rule, i.e. nonterminal substituted for multiple new symbols
        '''
        canonical = {} # Initialise canonical dict
        for nonterminal, substitutions in rules.items():

            if not isinstance(nonterminal, str):
                raise TypeError(f'Nonterminal \'{nonterminal}\' must be a string.')
            if not isinstance(substitutions, Iterable):
                raise TypeError(f'Substitutions for nonterminal \'{nonterminal}\' must be iterable.')
            
            canonical_subs = [] # Substitutions to be converted, final type will be tuple[tuple[str, ...]]

            for sub in substitutions:
                if isinstance(sub, str):
                    # NOTE using tuple() directly would separate chars into individual entries, which is not intended
                    canonical_subs.append((sub,))

                elif isinstance(sub, Iterable):
                    # NOTE in this case `sub` will NOT be a string, since that is caught in above case
                    if not all(isinstance(symbol, str) for symbol in sub):
                        raise TypeError('All terminals and nonterminals must be strings.')
                    canonical_subs.append(tuple(sub))

                else:
                    raise TypeError(f'Substitution \'{sub}\' must be iterable.')
                
            # Sort rule bodies by default order: len-lex of symbols in sub
            # TODO is it actually sorting?
            canonical[nonterminal] = tuple(sorted(canonical_subs))
        return canonical

    # Establish terminals and nonterminals from rules
    def _extract(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        '''
        - initialise terminals and nonterminals as sets
        - iterate through rules
            - add each nonterminal (i.e. rule key) to nonterminals
            - for each substition in each nonterminal's list of substitutions, add all symbols in the substitution to terminals
                - NOTE nonterminals can yield other nonterminals, so these will be filtered out
        - filter out nonterminals from `terminals` to leave only true terminals
        - sort and convert to tuples for return
        - return `nonterminals`, `terminals`
        '''
        terminals = set()
        nonterminals = set()

        # Extract symbols from rules dict
        for nonterminal, substitutions in self.rules.items():
            nonterminals.add(nonterminal)
            for sub in substitutions:
                for symbol in sub:
                    terminals.add(symbol)

        # Filter nonterminals and empty symbol '' out of `terminals`
        terminals = {symbol for symbol in terminals if symbol not in nonterminals and symbol}

        # Ensure start nonterminal comes first in sort
        nonterminals = tuple(sorted(nonterminals, key=lambda s: (s != self.start, s)))
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
    
    # Rename symbols in CFG
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
                              rules: dict[str, tuple[tuple[str, ...], ...]], 
                              all_nonterminals: Container[str]) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - `target`: symbol to query presence of within substitutions
        - `rules`: map of rules to query
        - `all_nonterminals`: collection of all nonterminals of CFG, to check valid input

        Returns dict mapping nonterminals to ONLY its substitutions containing given `target` nonterminal
        - if a nonterminal has no rules containing target, then it does not have a key in dict
        '''
        # Check input
        if target not in all_nonterminals:
            raise ValueError(f'Symbol \'{target}\' must be a nonterminal.')
        
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
            # Merged tuple of initial and new rules, without duplicates
            updated = tuple(sorted(set(initial_rules[nonterminal]) | set(new_rules[nonterminal])))
            # Update substitutions in final rules map
            rules_return[nonterminal] = updated

        return rules_return
    
    # Return list of new rules with each occurrence of given nonterminal removed
    @staticmethod
    def _remove_occurences_of(target: str,
                              sub: tuple[str, ...]) -> tuple[tuple[str, ...], ...]:
        '''
        - `target`: nonterminal whose occurences are to be removed
        - `sub`: rule body to remove occurences from

        Returns tuple of new rule bodies with with each occurence of target removed
        - e.g. for target 'A' and sub 'uAv', return {'uv'}
        - e.g. for target 'A' and sub 'uAvAw', return {'uvAw', 'uAvw', 'uvw'}

        NOTE this function is NOT called when sub only consists of 'target'
        '''
        raise NotImplementedError # TODO !!! Tricky powerset iteration
    

    # Determine if there are any remaining bad ε-rules
    @staticmethod
    def _contains_bad_erules(rules: dict[str, tuple[tuple[str, ...], ...]],
                             start: str) -> bool:
        '''
        - if `rules` contains any sub of the form 'A -> ε' where 'A' != `start`, return True
        - else return False
        '''
        for nonterminal, substitutions in rules.items():
            if any(sub == ('',) for sub in substitutions) and nonterminal != start:
                return True
        return False

    # Return rules mapping with bad ε-rules removed
    @staticmethod
    def remove_bad_epsilon_rules(rules: dict[str, tuple[tuple[str, ...], ...]],
                                 all_nonterminals: Container[str],
                                 start: str,
                                 removed: set[str] = {}) -> dict[str, tuple[tuple[str, ...], ...]]:
        '''
        - `rules`: rules map to remove bad ε-rules from
        - `all_nonterminals`: collection of CFG's nonterminals (to pass to called helper)
        - `start`: CFG start nonterminal
        - `removed`: set of nonterminals 'A' for which rule 'A -> ε' was already removed (for recursion)
            - NOTE only need to track rule head, since '-> ε' already implied
        '''
        # Don't modify rules in-place
        rules_return = rules.copy()

        # Determine all nonterminals that have bad ε-rules (in particular NOT including start nonterminal)
        to_remove = set() # Set of nonterminals 'A' which have a rule 'A -> ε' 
        for nonterminal, substitutions in rules.items():
            if any(sub == ('',) for sub in substitutions) and nonterminal != start:
                to_remove.add(nonterminal)

        # Do replacement process for each nonterminal with bad e-rule
        for nonterminal in to_remove:
            # Remove original bad ε-rule from nonterminal's substitutions
            rules[nonterminal] = CFG._delete_sub_from_substitutions(('',), rules[nonterminal])
            removed.add(nonterminal)

            # Add new rules with nonterminal omitted
            
            # Maps nonterminals to its respective rules containing `nonterminal`
            rules_to_add_from = CFG._get_rules_containing(nonterminal, rules, all_nonterminals)

            # Maps nonterminals to their respective new rules with `nonterminal` omitted
            rules_to_add = {}
            
            # For each rule body, generate new rules with nonterminal omitted
            for head, substitutions in rules_to_add_from.items():
                for sub in substitutions:
                    # Edge case for rule 'head -> nonterminal'
                    if sub == (nonterminal,):
                        # Only add new e-rule if not already removed
                        if head not in removed:
                            _append_dict_value(head, '', rules_to_add)
                    # Case for NOT 'head -> nonterminal'
                    else:
                        new_rules = CFG._remove_occurences_of(nonterminal, sub)
                        for new_rule in new_rules:
                            _append_dict_value(head, new_rule, rules_to_add)

            # Convert list of new rules to tuple before adding
            rules_to_add = {key: tuple(val) for key, val in rules_to_add.items()}
            # Add new rules with nonterminal omitted
            rules_return = CFG._add_new_rules(rules_to_add, rules_return)

        # Check if another pass needed to remove added ε-rules
        # Likely will be needed at first, but should always terminate
        if CFG._contains_bad_erules(rules_return, start):
            rules_return = CFG.remove_bad_epsilon_rules(rules_return, all_nonterminals, start, removed)
        return rules_return

    # Return rules mapping with unit rules 'A -> B' removed
    @staticmethod
    def remove_unit_rules(rules: dict[str, tuple[tuple[str, ...], ...]],
                          all_nonterminals: Container[str],
                          start: str) -> dict[str, tuple[tuple[str, ...], ...]]:
        raise NotImplementedError
    
    # Return rules with all bodies converted to normal form by introducting new nonterminals
    @staticmethod
    def convert_proper_form(rules: dict[str, tuple[tuple[str, ...], ...]],
                            all_nonterminals: Container[str],
                            start: str) -> dict[str, tuple[tuple[str, ...], ...]]:
        raise NotImplementedError


    # Convert grammar to Chomsky normal form
    def to_chomsky_normal_form(self) -> 'CFG':
        new_start = disjoint_symbol('S', set(self.nonterminals) | set(self.terminals))

        raise NotImplementedError
    
        # Sketch outline
        new_rules = CFG.remove_bad_epsilon_rules(self.rules, self.nonterminals, self.start)
        new_rules = CFG.remove_unit_rules(new_rules, self.nonterminals, self.start)
        new_rules = CFG.convert_proper_form(new_rules, self.nonterminals, self.start)
        # Rule to yield initial start from new start
        new_rules[new_start] = ((self.start,),)
        
        return CFG(new_rules, new_start)





    