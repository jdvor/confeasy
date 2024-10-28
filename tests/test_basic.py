from __future__ import annotations

import confeasy


def test_filter_data():
    actual = confeasy._filter_data("alpha", {"alpha.one": 1, "alpha.two": 2, "beta": 3})
    expected = {"one": 1, "two": 2}
    assert expected.keys() == actual.keys()


def test_bind_1():
    obj = Alpha()
    expected = "John"
    ok = confeasy._bind(obj, "first_name", expected, 0)
    actual = obj.first_name
    assert ok
    assert expected == actual


def test_bind_2():
    obj = Alpha()
    expected = "Doe"
    ok = confeasy._bind(obj, "surname", expected, 0)
    actual = obj.surname
    assert ok
    assert expected == actual


def test_bind_3():
    obj = Alpha()
    expected = "apple"
    ok = confeasy._bind(obj, "beta.fruit", expected, 0)
    actual = obj.beta.fruit
    assert ok
    assert expected == actual


def test_bind_4():
    obj = Alpha()
    expected = 6.75
    ok = confeasy._bind(obj, "beta.gamma.ratio", expected, 0)
    actual = obj.beta.gamma.ratio
    assert ok
    assert expected == actual


def test_bind_5():
    obj = Alpha()
    ok = confeasy._bind(obj, "beta.non_existent", 666, 0)
    assert not ok


class Alpha:
    def __init__(self):
        self._first_name: str = ""
        self.surname: str = ""
        self._beta: Beta = Beta()

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        self._first_name = value

    @property
    def beta(self) -> Beta:
        return self._beta

    @beta.setter
    def beta(self, value: Beta) -> None:
        self._beta = value


class Beta:
    def __init__(self):
        self._fruit: str = "orange"
        self.gamma: Gamma = Gamma()

    @property
    def fruit(self) -> str:
        return self._fruit

    @fruit.setter
    def fruit(self, value: str) -> None:
        self._fruit = value


class Gamma:
    def __init__(self):
        self.ratio: float = 0.0
        self.increment: int = 1
