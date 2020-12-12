from compiler.statement import Statement
from typing import Union, List


StatementsType = Union[List[Statement], Statement]


class Statements:
    def __init__(self, value: StatementsType):
        if isinstance(value, Statement):
            self.value = [value]
        elif isinstance(value, list) and all(isinstance(item, Statement) for item in value):
            self.value = value
        else:
            raise TypeError('value must be instance of Statement or list of Statements')

    @staticmethod
    def create(value):
        if isinstance(value, Statements):
            return value

        return Statements(value)

    def __add__(self, other):
        other = Statements.create(other)

        return Statements.create([*self.value, *other.value])

    def __mul__(self, other):
        other = Statements.create(other)
        # TODO implement me

    def __repr__(self):
        return ' | '.join(map(lambda statement: str(statement), self.value))

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        try:
            value = self.value[self._i]
        except IndexError:
            raise StopIteration

        self._i += 1
        return value