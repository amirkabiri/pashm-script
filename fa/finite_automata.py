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
        self.states = states
        self.symbols = symbols
        self.start = start
        self.terminals = terminals
        self.transitions = transitions
        self.value = self.create_value()

    def calculate_symbols(self):
        symbols = []

        for transition in self.transitions:
            symbol: Symbol = transition[1].value

            if symbol not in symbols:
                symbols.append(symbol)

        return symbols

    def create_value(self):
        value = dict(map(
            lambda state: [
                state.value,
                    dict(list(map(lambda symbol: [str(symbol), []], self.symbols)) + [['', []]])
            ],
            self.states
        ))

        for transition in self.transitions:
            start = transition[0].value
            end = transition[2].value
            symbol = str(transition[1])

            value[start][symbol].append(end)

        return value

    def get_symbol_by_char(self, char):
        symbols = self.get_symbols_by_char(char)

        if len(symbols) == 0:
            return None

        return symbols[0]

    def get_symbols_by_char(self, char):
        return list(filter(lambda symbol: symbol.check(char), self.symbols))

    def has_state(self, state: State):
        return any(state.value == s.value for s in self.states)

    def is_terminal(self, state: State):
        return any(state.value == s.value for s in self.terminals)

    def __repr__(self):
        pass


w = CharSet().range(65, 91).range(97, 123).range(48, 58)
fa = FiniteAutomata(
    [State('1'), State('2'), State('3'), State('4'), State('5'), State('6')],
    [Symbol(w), Symbol('@'), Symbol('.')],
    State('1'),
    [State('6')],
    [
        [State('1'), Symbol(w), State('2')],
        [State('2'), Symbol(w), State('2')],
        [State('2'), Symbol('.'), State('1')],
        [State('2'), Symbol('@'), State('3')],
        [State('3'), Symbol(w), State('4')],
        [State('4'), Symbol(w), State('4')],
        [State('4'), Symbol('.'), State('5')],
        [State('5'), Symbol(w), State('6')],
        [State('6'), Symbol(w), State('6')],
        [State('6'), Symbol('.'), State('5')],
    ]
)


print(fa.value)