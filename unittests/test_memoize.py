from pypi2nix.memoize import memoize


def test_memoized_method_returns_correct_result():
    class A:
        @memoize
        def x(self):
            return 1

    assert A().x() == 1


def test_memoized_method_gets_called_only_once():
    class A:
        def __init__(self):
            self.times_called = 0

        @memoize
        def x(self):
            self.times_called += 1
            return

    a = A()
    a.x()
    a.x()
    assert a.times_called == 1
