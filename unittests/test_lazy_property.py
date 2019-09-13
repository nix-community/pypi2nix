from pypi2nix.lazy_property import lazy_property


def test_lazy_property_returns_correct_result():
    class A:
        @lazy_property
        def x(self):
            return 1

    assert A().x == 1


def test_lazy_property_gets_called_only_once():
    class A:
        def __init__(self):
            self.times_called = 0

        @lazy_property
        def x(self):
            self.times_called += 1
            return

    a = A()
    a.x
    a.x
    assert a.times_called == 1
