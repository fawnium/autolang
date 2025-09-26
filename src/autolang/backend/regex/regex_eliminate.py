# Iterative-scan parser that is called by `GNFA` to decide how to eliminate operators from edge labels
class RegexParserEliminate:
    '''
    - input regex string
    - trim reduntant brackets enclosing entire string, if present
    - return early if string is primitive with `('primitive', tuple())`
    - parse through input and identify leftmost, top-level, highest precedence operator to be eliminated
        - leftmost means the first occuring in the string
        - top-level means not embedded inside any brackets
        - highest precedence means `+` first, then `.`, then `*` last
            - for example with 'a.b+c', the leftmost operator is `.`, but `+` should be what is returned due to precedence
    - decide return depending on which operator is identified:
        - if `+`, slice string into R1 and R2 (omitting `+` literal), and return `('union', (R1, R2))`
        - if '.', do the same as above, and return `('concat', (R1, R2))`
        - if '*', backtrack to identify correct operand (either literal or bracketed group) R, and return `('star', (R,))`
    '''
    def __init__(self):
        pass

    # Remove brackets enclosing entire string, if present
    @staticmethod
    def trim_enclosing_brackets(R: str) -> str:
        if R == '': return R # Empty string edge case
        while R.startswith('(') and R.endswith(')'): # Run loop once for each pair of enclosing brackets
            depth = 0
            for i, c in enumerate(R):
                if c == '(':
                    depth += 1
                elif c == ')':
                    depth -= 1
                if depth == 0: # If top-level bracket has closed
                    if i == len(R) - 1: # If top bracket is totally-enclosing
                        R = R[1:-1] # Trim and return to check for another layer
                        break
                    else: # If top bracket doesn't enclose whole string
                        return R # There can be no other totally-enclosing layers
        return R

    # Main parse method
    @staticmethod
    def parse(R: str) -> tuple[str, tuple[str, ...]]:
        # Strip enclosing brackets
        R = RegexParserEliminate.trim_enclosing_brackets(R)
        # Early return for primitive regex
        if ('+' not in R) and ('.' not in R) and ('*' not in R):
            return ('primitive', tuple())
        # Look for '+'
        depth = 0
        for i, c in enumerate(R):
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            elif depth == 0 and c == '+':
                # Slice R into two halves excluding '+' that is eliminated
                regex1 = R[:i]
                regex2 = R[i+1:]
                return ('union', (regex1, regex2))
        # Look for '.'
        for i, c in enumerate(R):
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            elif depth == 0 and c == '.':
                # Slice R into two halves excluding '.' that is eliminated
                regex1 = R[:i]
                regex2 = R[i+1:]
                return ('concat', (regex1, regex2)) 
        # Look for '*'
        if R.endswith('*'):
            regex = R[:-1]
            return ('star', (regex,)) # Star must apply to the entire string before it, because no '+' or '.' was found before
        return None # This should never happen unless input string was invalid
                
