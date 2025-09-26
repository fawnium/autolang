# Special chars forbidden from being in an alphabet
OP_CHARS = '()+*. '

# Recursive descent parser to handle input regex and ensure syntax is valid
class RegexParserInput:

    # NOTE this parser will *reejct* the empty regex ''
    # But `is_valid_regex` will not call `RegexParserInput` in this case, so '' is still valid globally

    '''
    Each method below corresponds to a rule in the grammar of the language of regular expressions
    '''

    def __init__(self, R: str):
        self.R = R.replace(' ', '') # Remove spaces from input regex
        self.alphabet = alphabet_of(R)
        self.pos = 0

    def parse(self) -> bool:
        result = self.parse_union()
        if self.pos != len(self.R):
            raise SyntaxError('Unexpected characters in regular expression.')
        return result

    def parse_union(self) -> bool:
        self.parse_concat()
        while self.peek() == '+':
            self.consume('+')
            self.parse_concat()
        return True

    def parse_concat(self) -> bool:
        if not self.parse_star():
            raise SyntaxError('Expected expression in concatenation, but none seen.')
        while True:
            if not self.peek() or self.peek() in ')+': # Exit if next symbol cannot start new atom
                break
            if not self.parse_star():
                break
        return True

    def parse_star(self) -> bool:
        self.parse_atom()
        if self.peek() == '*':
            self.consume('*')
        return True

    def parse_atom(self) -> bool:
        if self.peek() == '(':
            self.consume('(')
            self.parse_union() # Parse newly opened bracket
            if self.peek() != ')':
                raise SyntaxError('Expected closing bracket \')\'.')
            self.consume(')')
        elif self.peek() in self.alphabet:
            self.consume(self.peek())
        else:
            raise SyntaxError(f'Unexpected symbol \'{self.peek()}\' at position \'{self.pos}\'.')
        return True

    def peek(self) -> str:
        return self.R[self.pos] if self.pos < len(self.R) else None

    def consume(self, letter) -> None:
        if self.peek() != letter:
            raise SyntaxError(f'Expected \'{letter}\' at position {self.pos} but saw \'{self.peek()}\'.')
        self.pos += 1

# Wrapper that calls `RegexParserInput` to validate syntax of regex
def is_valid_regex(R: str) -> bool:
    if R == '': return True # Edge case for empty regex
    try:
        RegexParserInput(R).parse()
        return True
    except SyntaxError as e:
        # print(f'Regex {R} is invalid: {e}')
        return False

# Extracts and returns the alphabet of a regex
def alphabet_of(R: str) -> tuple[str, ...]:
    alphabet = set()
    for letter in R:
        if letter not in OP_CHARS: # Brackets and operators and spaces cannot be in alphabet, but assume every other character is
            alphabet.add(letter)
    return tuple(alphabet)

# Preprocess regex by explicitly adding concat operator `.`
def add_concat(R: str) -> str:
    '''
    The following are all of the pairs of symbols between which the concat operator `.` must be inserted:
    1 - letter . letter
    2 - letter . (
    3 - ) . letter
    4 - ) . (
    5 - * . letter
    6 - * . (
    Other places, such as 'letter . +', or 'letter . *', should not have a concat added.
    '''
    alphabet = alphabet_of(R) # Get alphabet
    result = [] # Final processed regex
    for i, char in enumerate(R):
        result.append(char)
        if i + 1 < len(R): # Only proceed if there is a next char in regex
            next_char = R[i + 1]
            if (char in alphabet or char in ')*') and (next_char in alphabet or next_char == '('):
                result.append('.') # Add `.` between current and next character, if one of the six conditions in docstring is true
    return ''.join(result) # Return re-assembled regex


