from compiler.fa.finite_automata import FiniteAutomata
from compiler.fa.atom import Symbol, State


class NFARunner:
    def __init__(self, fa: FiniteAutomata):
        self.fa = fa
        self.current = [fa.start.value]

    def read(self, char: str):
        symbols = self.fa.get_symbols_by_char(char)

        next_cursors = []
        for cursor in self.current:
            for symbol in symbols:
                try:
                    next_cursors = next_cursors + self.fa.value[cursor][str(symbol)]
                except:
                    pass

        if len(next_cursors) == 0:
            raise Exception('stuck')

        self.current = next_cursors
        return self

    def move(self, state):
        if not self.fa.has_state(State(state)):
            raise KeyError('state not exists')

        self.current = state
        return self

    @property
    def accepted(self):
        return any(self.fa.is_terminal(State(cursor)) for cursor in self.current)

    def __repr__(self):
        return 'current: ' + self.current + ' & accepted: ' + str(self.accepted)

    @staticmethod
    def run(fa, input):
        matched = []
        i = 0

        while i < len(input):
            dfa_runner = NFARunner(fa)
            j = i
            found = ''
            accepted_string = ''

            while j < len(input):
                try:
                    dfa_runner.read(input[j])
                except Exception:
                    print('stuck', [(found + input[j]).replace('\n', '/n'), accepted_string])
                    break

                found += (input[j])
                j += 1

                if dfa_runner.accepted:
                    accepted_string = found
                    print('accepted', accepted_string)

            if len(accepted_string):
                matched.append([i, accepted_string])
                i += len(accepted_string)
            else:
                i += 1

        return dict(matched)