from compiler.char_set import CharSet
from compiler.fa.finite_automata import FiniteAutomata
from compiler.fa.atom import State, Symbol
from compiler.fa.multi_dfa_runner import MultiDFARunner


def build_assign_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(3)],
        [Symbol(':'), Symbol('=')],
        State('0'),
        [State('2')],
        [
            [State('0'), Symbol(':'), State('1')],
            [State('1'), Symbol('='), State('2')],
        ]
    )


def build_multiply_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('*')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('*'), State('1')],
        ]
    )


def build_add_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('+')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('+'), State('1')],
        ]
    )


def build_open_par_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('(')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('('), State('1')],
        ]
    )


def build_close_par_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol(')')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol(')'), State('1')],
        ]
    )


def build_variable_dfa():
    first_char = CharSet().range(65, 91).range(97, 123).char('_')
    rest_chars = CharSet().range(65, 91).range(97, 123).range(48, 58).char('_')

    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol(first_char), Symbol(rest_chars)],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol(first_char), State('1')],
            [State('1'), Symbol(rest_chars), State('1')],
        ]
    )


def build_number_dfa():
    chars = CharSet().range(48, 58)
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol(chars)],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol(chars), State('1')],
            [State('1'), Symbol(chars), State('1')],
        ]
    )


machines = [
    build_assign_dfa(),
    build_multiply_dfa(),
    build_add_dfa(),
    build_open_par_dfa(),
    build_close_par_dfa(),
    build_variable_dfa(),
    build_number_dfa(),
]
tokens = [
    { "type": "operator" },
    { "type": "operator" },
    { "type": "operator" },
    { "type": "par" },
    { "type": "par" },
    { "type": "variable" },
    { "type": "number" },
]


def scanner(content):
    result_tokens = []

    def on_match(result, index):
        nonlocal result_tokens
        token = tokens[list(result.keys())[0]]
        result_tokens.append({**token, "value": list(result.values())[0]})

        r = [len(value) for value in result.values()]
        return max(r)

    MultiDFARunner.run(
        machines,
        content,
        on_match
    )

    return result_tokens