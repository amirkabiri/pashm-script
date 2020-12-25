from __future__ import annotations
from typing import Union
from json import dumps
from copy import deepcopy


class CharSet:
    def __init__(self):
        self._value = []
        self._every = False

    def clone(self):
        obj = CharSet()
        obj._value = deepcopy(self._value)
        obj._every = self._every
        return obj

    def range(self, start: int, end: int) -> CharSet:
        self._value.append({'type': 'range', 'value': [start, end]})
        return self

    def not_range(self, start: int, end: int) -> CharSet:
        self._value.append({'type': 'not_range', 'value': [start, end]})
        return self

    def char(self, char: Union[int, str]) -> CharSet:
        if isinstance(char, str):
            char = ord(char[0])

        self._value.append({'type': 'range', 'value': [char, char + 1]})
        return self

    def not_char(self, char: Union[int, str]) -> CharSet:
        if isinstance(char, str):
            char = ord(char[0])

        self._value.append({'type': 'not_range', 'value': [char, char + 1]})
        return self

    def every(self) -> CharSet:
        self._every = True
        return self

    def check(self, char: Union[int, str]) -> bool:
        if isinstance(char, str):
            char = ord(char[0])

        accepted = self._every

        for rule in self._value:
            type = rule['type']
            value = rule['value']

            if type == 'range':
                if value[0] <= char < value[1]:
                    accepted = True
                    continue
            elif type == 'not_range':
                if value[0] <= char < value[1]:
                    accepted = False

        return accepted

    def all(self):
        result = []

        for rule in self._value:
            if rule['type'] == 'range':
                for i in range(rule['value'][0], rule['value'][1]):
                    result.append(i)
            elif rule['type'] == 'not_range':
                for i in range(rule['value'][0], rule['value'][1]):
                    result.remove(i)

        return result

    def __repr__(self):
        return dumps([self._every, self._value])