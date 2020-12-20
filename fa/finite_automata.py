from typing import Union, List

from compiler.char_set import CharSet
from compiler.fa.atom import Symbol, State


class FiniteAutomata:
    def __init__(
            self,
            states: List[State],
            symbols: List[Symbol],
            start: State,
            terminals: List[State],
            transitions
    ):
        self.states = list(map(lambda state: state.value, states))
        self.symbols = self.create_symbols(symbols)
        self.start = start.value
        self.terminals = list(map(lambda state: state.value, terminals))
        self.transitions = transitions
        self.table = self.create_table()

    def create_symbols(self, symbols):
        result = []

        for symbol in symbols:
            result = result + symbol.value.all()

        return list(set(map(lambda ascii: chr(ascii), result)))

    def create_table(self):
        value = dict(map(lambda state: [state, dict(map(
            lambda symbol: [symbol, []],
            self.symbols
        ))],self.states))

        for transition in self.transitions:
            start = transition[0].value
            end = transition[2].value

            for ascii in transition[1].value.all():
                value[start][chr(ascii)].append(end)

        return value

    def has_state(self, state):
        return state in self.states

    def is_terminal(self, state):
        return state in self.terminals