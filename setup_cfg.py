from autolang.backend.cfg.cfg import CFG

'''
Some CFGs for testing, from Sipser
'''

rules1 = {'A': [['0','A','1'], 'B'],
          'B': ['#']}

cfg1 = CFG(rules1, 'A')



rules2 = {'<SENTENCE>':    [['<NOUN-PHRASE>', '<VERB-PHRASE>']],
          '<NOUN-PHRASE>': ['<CMPLX-NOUN>', ['<CMPLX-NOUN>', '<PREP-PHRASE>']],
          '<VERB-PHRASE>': ['<CMPLX-VERB>', ['<CMPLX-VERB>', '<PREP-PHRASE>']],
          '<PREP-PHRASE>': [['<PREP>', '<CMPLX-NOUN>']],
          '<CMPLX-NOUN>':  [['<ARTICLE>', '<NOUN>']],
          '<CMPLX-VERB>':  ['<VERB>', ['<VERB>', '<NOUN-PHRASE>']],
          '<ARTICLE>':     ['a', ['the']], # Mixed single symbols
          '<NOUN>':        [['boy'], ['girl'], ['flower']], # All symbols wrapped
          '<VERB>':        [['touches'], ['likes'], ['sees']], # All symnbols wrapped
          '<PREP>':        ['with']}
cfg2 = CFG(rules2, '<SENTENCE>')


rules3 = {'S': [['a','S','b'], ['S','S'], '']}
cfg3 = CFG(rules3, 'S')


rules4 = {'<EXPR>': [['<EXPR>', '+', '<TERM>'], '<TERM>'],
          '<TERM>': [['<TERM>', '*', '<FACTOR>'], '<FACTOR>'],
          '<FACTOR>': [['(', '<EXPR>', ')'], 'a']}
cfg4 = CFG(rules4, '<EXPR>')

# Ambiguous version of cg4
rules5 = {'<EXPR>': [['<EXPR>', '+', '<EXPR>'], ['<EXPR>', '*', '<EXPR>'], ['(', '<EXPR>', ')'], 'a']}
cfg5 = CFG(rules5, '<EXPR>')