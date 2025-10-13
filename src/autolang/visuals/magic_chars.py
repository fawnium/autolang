'''
Define set of resusable constant chars for visually formatting transition tables

See https://en.wikipedia.org/wiki/Box-drawing_characters
'''

# Straight lines
V = '║' # Vertical line
H = '═' # Horizontal line
# Corners - (U)p (D)own (L)eft (R)ight
# NOTE included directions are where the lines are pointing to
UL = '╝'
UR = '╚'
DL = '╗'
DR = '╔'
# Junctions
UDL = '╣'
UDR = '╠'
ULR = '╩'
DLR = '╦'
UDLR = '╬'
# Special chars
EPSILON = 'ε'
EMPTY = '∅'

# Right arrow for diagram edge labels
RIGHT_ARROW = '→'