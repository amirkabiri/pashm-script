from compiler.grammar.expression import Expression
from typing import Union, List


StatementType = Union[Expression, List[Expression]]


class Statement:
    def __init__(self, value: StatementType):
        if isinstance(value, Expression):
            self.value = [value]
        elif isinstance(value, list) and all(isinstance(item, Expression) for item in value):
            self.value = value
        else:
            raise TypeError('value must be instance of Expression or list of Expressions')

    @staticmethod
    def create(value):
        if isinstance(value, Statement):
            return value

        return Statement(value)

    def __getattr__(self, item):
        print('__getattr__', item)
        pass

    def __repr__(self):
        return ''.join(map(lambda exp: str(exp), self.value))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.value[key.start:key.stop:key.step]
        return self.value[key]

    def __len__(self):
        return len(self.value)

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

    # def __add__(self, other):
    #     other = Statement.create(other)
    #
    #     return Statement.create([*self.value, *other.value])
    #
    # def __mul__(self, other):
    #     pass