
class CFG:

    def __init__(self,
                 rules: dict[str, tuple[tuple[str, ...]]],
                 start: str):
        
        #self.validate_rules(rules, start)

        self.rules = rules
        self.start = start
        self.nonterminals, self.terminals = self.extract()

    # Ensure rules dict is correctly formatted
    def validate_rules(self, rules, start) -> bool:
        raise NotImplementedError

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
            for substitution in substitutions:
                for symbol in substitution:
                    terminals.add(symbol)

        # Filter nonterminals out of `terminals`
        terminals = {symbol for symbol in terminals if symbol not in nonterminals}

        # Ensure start nonterminal comes first in sort
        nonterminals = tuple(sorted(nonterminals, key=lambda s: (s != self.start, s)))
        terminals = tuple(sorted(terminals))
        return nonterminals, terminals
    
    def __repr__(self):
        repr_str = 'CFG(\n'
        for nonterminal, substitutions in self.rules.items():
            repr_str += nonterminal + ' ::= '
            repr_str += ' | '.join(''.join(substitution) for substitution in substitutions)
            repr_str += '\n'
        repr_str += ')'
        return repr_str
    
    def __str__(self):
        return self.__repr__()
        #return 'CFG with nonterminals {' + ','.join(self.nonterminals) + '} and terminals {' + ','.join(self.terminals) + '}'

        



    