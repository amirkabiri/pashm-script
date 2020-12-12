from compiler.char_set import CharSet
from typing import Union


class Atom:
    def __init__(self, value: Union[str, CharSet]):
        self.value = value

    def __repr__(self):
        return self.value


class State(Atom):
    def __init__(self, value: Union[str, CharSet]):
        super().__init__(value)

    def __eq__(self, other):
        return isinstance(other, State) and self.value == other.value


class Symbol(Atom):
    def __init__(self, value: Union[str, int, CharSet]):
        if not isinstance(value, CharSet):
            value = CharSet().char(value)

        super().__init__(value)

    def check(self, value: Union[str, int]) -> bool:
        return self.value.check(value)

    def __repr__(self):
        if not hasattr(self, '__str'):
            self.__str = str(self.value)


        return self.__str