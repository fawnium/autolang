from autolang.backend.utils import disjoint_symbol
from autolang.visuals.utils_visuals import eps

from collections.abc import Iterable

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
                
            canonical[nonterminal] = tuple(canonical_subs)
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
        for nonterminal, substitutions in self.rules.items():
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




    