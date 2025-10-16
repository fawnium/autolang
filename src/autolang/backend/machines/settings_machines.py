

# Max length to generate words up to if none given
DEFAULT_LANGUAGE_LENGTH = 5

# Characters forbidden from being alphabet letters or in state names
'''
NOTE this is a tricky problem and is not handled very well
- the main reason for banning chars is to prevent conflicts with regex operators
    - e.g. if '+' is in an alphabet, then the regex parser cannot determine 
      which instance is a union operator, and which is a letter
- the other reason is because '_' is reserved for TM tape, but this is pointless 
  since this is not even enforced for TM
- There is another general problem, which is that letters can only be single 
  chars in current implementation
    - many practical FSA use 'symbols' that consist of multiple chars

TODO overhaul handling of allowed symbols, probably make model-specific

'''
FORBIDDEN_CHARS = ['.', '+', '*', '_', ' ']

# Default reserved names for TMs
DEFAULT_TM_ACCEPT = 'qa'
DEFAULT_TM_REJECT = 'qr'
DEFAULT_TM_BLANK = '_'
DEFAULT_TM_LEFT = 'L'
DEFAULT_TM_RIGHT = 'R'
DEFAULT_TM_NEUTRAL = 'N' # NOTE unused

# Arbitrary limit to computation steps in case of non-halting with no infinite loops detected
DEFAULT_TM_MAX_STEPS = int(1e8) # Default 100 million
