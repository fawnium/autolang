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
        self.rules = self.canonise_rules(rules)
        
        # Check start is listed as a nonterminal
        if start not in rules:
            raise ValueError(f'Start symbol \'{start}\' must be listed in rules.')
        self.start = start

        # Extract symbol sets
        self.nonterminals, self.terminals = self.extract()

    # Ensure rules dict is correctly formatted and convert containers to tuples for consistency
    def canonise_rules(self, rules: dict[str, Iterable[Iterable[str] | str]]) -> dict[str, tuple[tuple[str, ...], ...]]:
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
                    if not all(isinstance(symbol, str) for symbol in sub):
                        raise TypeError('All terminals and nonterminals must be strings.')
                    canonical_subs.append(tuple(sub))

                else:
                    raise TypeError(f'Substitution \'{sub}\' must be iterable.')
                
            canonical[nonterminal] = tuple(canonical_subs)
        return canonical

    # Establish terminals and nonterminals from rules
    def extract(self) -> tuple[tuple[str, ...], tuple[str, ...]]:
        '''
        - initialise terminals and nonterminals as sets
        - iterate through rules
            - add each nonterminal (i.e. rule key) to nonterminals
            - for each substition in each terminal's list of substitutions, add all symbols in the substitution to terminals
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
            repr_str += ' | '.join(''.join(eps(symbol) for symbol in substitution) for substitution in substitutions)
            repr_str += '\n'
        repr_str += ')'
        return repr_str
    
    def __str__(self):
        return 'CFG with nonterminals {' + ','.join(self.nonterminals) + '} and terminals {' + ','.join(self.terminals) + '}'

        



    