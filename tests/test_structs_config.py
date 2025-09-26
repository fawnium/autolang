import unittest
from autolang.backend.machines.structs_config import ConfigNFA, ConfigPDA, ConfigTM


class TestConfigNFA(unittest.TestCase):

    def test_init_defaults(self):
        config = ConfigNFA('q0', 'abc')
        self.assertEqual(config.state, 'q0')
        self.assertEqual(config.suffix, 'abc')
        self.assertEqual(config.path, tuple())

    def test_eq_and_hash(self):
        a = ConfigNFA('q0', 'abc')
        b = ConfigNFA('q0', 'abc') # Same as `a`
        c = ConfigNFA('q1', 'abc') # Different in first arg
        d = ConfigNFA('q0', 'ab') # Different in second arg
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertEqual(hash(a), hash(b))
        self.assertNotEqual(hash(a), hash(c))
        self.assertNotEqual(hash(a), hash(d))

    def test_repr(self):
        # Test string containment instead of exact string, in case repr format changes in the future
        config = ConfigNFA('q0', 'bcd', path = (('q0', 'a'), ('q1', 'b')))
        self.assertIn('ConfigNFA', repr(config))
        self.assertIn('q0', repr(config))
        self.assertIn('bcd', repr(config))


class TestConfigPDA(unittest.TestCase):

    def test_init_defaults(self):
        config = ConfigPDA('q0', 'abc')
        self.assertEqual(config.state, 'q0')
        self.assertEqual(config.suffix, 'abc')
        self.assertEqual(config.stack, '')
        self.assertEqual(config.path, tuple())

    def test_eq_and_hash(self):
        a = ConfigPDA('q0', 'abc', 'x')
        b = ConfigPDA('q0', 'abc', 'x') # Same as `a`
        c = ConfigPDA('q1', 'abc', 'x') # Different in first arg
        d = ConfigPDA('q0', 'ab', 'x') # Different in second arg
        e = ConfigPDA('q0', 'abc', 'xy') # Different in third arg
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        self.assertEqual(hash(a), hash(b))
        self.assertNotEqual(hash(a), hash(c))
        self.assertNotEqual(hash(a), hash(d))
        self.assertNotEqual(hash(a), hash(e))

    def test_repr(self):
        # Test string containment instead of exact string, in case repr format changes in the future
        config = ConfigPDA('q0', 'abc', 'ax', path = (('q0', 'a', ''), ('q1', 'b', 'x')))
        self.assertIn('ConfigPDA', repr(config))
        self.assertIn('q0', repr(config))
        self.assertIn('abc', repr(config))
        self.assertIn('ax', repr(config))


class TestConfigTM(unittest.TestCase):

    def test_head_negative(self):
        config = ConfigTM('q0', list('abc'), -1)
        self.assertEqual(config.head, 0)

    def test_eq_and_hash(self):
        a = ConfigTM('q0', list('abc_'), 1)
        b = ConfigTM('q0', list('abc_'), 1) # Same as `a`
        c = ConfigTM('q0', list('abc_'), 1, (('q0', 'a'),)) # Same as `a` but different path - should be equal anyway
        d = ConfigTM('q1', list('abc_'), 1) # Different first arg
        e = ConfigTM('q0', list('abc'), 1) # Different second arg
        f = ConfigTM('q0', list('abc_'), 2) # Different third arg
        self.assertEqual(a, b)
        self.assertEqual(a, c)
        self.assertNotEqual(a, d)
        self.assertNotEqual(a, e)
        self.assertNotEqual(a, f)
        self.assertEqual(hash(a), hash(b))
        self.assertEqual(hash(a), hash(c))
        self.assertNotEqual(hash(a), hash(d))
        self.assertNotEqual(hash(a), hash(e))
        self.assertNotEqual(hash(a), hash(f))

    def test_repr_head_placement(self):
        config = ConfigTM('q1', list('abc'), 1)
        self.assertEqual(str(config), 'a(q1)bc')
    
    def test_repr_appends_blank(self):
        config = ConfigTM('q1', list('abc'), 3)
        self.assertEqual(str(config), 'abc(q1)_')


if __name__ == '__main__':
    unittest.main()
