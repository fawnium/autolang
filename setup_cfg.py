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