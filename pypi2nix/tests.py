try:
    import unittest2 as unittest
except ImportError:
    import unittest
    assert unittest


class TestPython2Nix(unittest.TestCase):

    def test_(self):
        assert False
