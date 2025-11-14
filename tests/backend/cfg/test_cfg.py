import unittest

from autolang.backend.cfg.cfg import CFG

class TestCanoniseRules(unittest.TestCase):

    def test_single_unit_rule(self):
        rules = {'A': ['A']}
        out = CFG._canonise_rules()