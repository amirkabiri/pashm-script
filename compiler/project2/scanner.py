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


def build_divide_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('/')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('/'), State('1')],
        ]
    )


def build_pow_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('^')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('^'), State('1')],
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


def build_minus_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('-')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('-'), State('1')],
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
    digits = CharSet().range(48, 58)

    return FiniteAutomata(
        [State(str(i)) for i in range(4)],
        [Symbol(digits), Symbol('.')],
        State('0'),
        [State('1'), State('3')],
        [
            [State('0'), Symbol(digits), State('1')],
            [State('1'), Symbol(digits), State('1')],
            [State('1'), Symbol('.'), State('2')],
            [State('2'), Symbol(digits), State('3')],
            [State('3'), Symbol(digits), State('3')],
        ]
    )


def build_open_brace_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('{')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('{'), State('1')],
        ]
    )


def build_close_brace_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol('}')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol('}'), State('1')],
        ]
    )


def build_params_delimiter_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol(',')],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol(','), State('1')],
        ]
    )


def build_function_dfa():
    first_char = CharSet().range(65, 91).range(97, 123).char('_')
    rest_chars = CharSet().range(65, 91).range(97, 123).range(48, 58).char('_')

    return FiniteAutomata(
        [State(str(i)) for i in range(3)],
        [Symbol(first_char), Symbol(rest_chars), Symbol('(')],
        State('0'),
        [State('2')],
        [
            [State('0'), Symbol(first_char), State('1')],
            [State('1'), Symbol(rest_chars), State('1')],
            [State('1'), Symbol('('), State('2')],
        ]
    )


def build_while_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(6)],
        [
            Symbol('w'), Symbol('h'), Symbol('i'), Symbol('l'), Symbol('e')
        ],
        State('0'),
        [State('5')],
        [
            [State('0'), Symbol('w'), State('1')],
            [State('1'), Symbol('h'), State('2')],
            [State('2'), Symbol('i'), State('3')],
            [State('3'), Symbol('l'), State('4')],
            [State('4'), Symbol('e'), State('5')],
        ]
    )


def build_do_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(3)],
        [
            Symbol('d'), Symbol('o')
        ],
        State('0'),
        [State('2')],
        [
            [State('0'), Symbol('d'), State('1')],
            [State('1'), Symbol('o'), State('2')],
        ]
    )


def build_if_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(3)],
        [
            Symbol('i'), Symbol('f')
        ],
        State('0'),
        [State('2')],
        [
            [State('0'), Symbol('i'), State('1')],
            [State('1'), Symbol('f'), State('2')],
        ]
    )


def build_else_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(5)],
        [
            Symbol('e'), Symbol('l'), Symbol('s'), Symbol('e'),
        ],
        State('0'),
        [State('4')],
        [
            [State('0'), Symbol('e'), State('1')],
            [State('1'), Symbol('l'), State('2')],
            [State('2'), Symbol('s'), State('3')],
            [State('3'), Symbol('e'), State('4')],
        ]
    )


def build_delimiter_dfa():
    return FiniteAutomata(
        [State(str(i)) for i in range(2)],
        [Symbol(";")],
        State('0'),
        [State('1')],
        [
            [State('0'), Symbol(";"), State('1')],
        ]
    )


machines = [
    {
        "dfa": build_assign_dfa(),
        "priority": 100,
        "token": {"type": "operator"}
    },
    {
        "dfa": build_multiply_dfa(),
        "priority": 100,
        "token": {"type": "operator"}
    },
    {
        "dfa": build_divide_dfa(),
        "priority": 100,
        "token": {"type": "operator"}
    },
    {
        "dfa": build_pow_dfa(),
        "priority": 100,
        "token": {"type": "operator"}
    },
    {
        "dfa": build_add_dfa(),
        "priority": 100,
        "token": {"type": "operator"}
    },
    {
        "dfa": build_minus_dfa(),
        "priority": 100,
        "token": {"type": "operator"}
    },

    {
        "dfa": build_variable_dfa(),
        "priority": 40,
        "token": {"type": "variable"}
    },
    {
        "dfa": build_number_dfa(),
        "priority": 40,
        "token": {"type": "number"}
    },

    {
        "dfa": build_open_brace_dfa(),
        "priority": 100,
        "token": {"type": "brace"}
    },
    {
        "dfa": build_close_brace_dfa(),
        "priority": 100,
        "token": {"type": "brace"}
    },

    {
        "dfa": build_open_par_dfa(),
        "priority": 100,
        "token": {"type": "par"}
    },
    {
        "dfa": build_close_par_dfa(),
        "priority": 100,
        "token": {"type": "par"}
    },

    {
        "dfa": build_delimiter_dfa(),
        "priority": 100,
        "token": {"type": "delimiter"}
    },

    {
        "dfa": build_function_dfa(),
        "priority": 70,
        "token": {"type": "function"}
    },
    {
        "dfa": build_params_delimiter_dfa(),
        "priority": 100,
        "token": {"type": "params_delimiter"}
    },

    {
        "dfa": build_while_dfa(),
        "priority": 80,
        "token": {"type": "while"}
    },
    {
        "dfa": build_do_dfa(),
        "priority": 80,
        "token": {"type": "do"}
    },

    {
        "dfa": build_if_dfa(),
        "priority": 80,
        "token": {"type": "if"}
    },
    {
        "dfa": build_else_dfa(),
        "priority": 80,
        "token": {"type": "else"}
    },
]


def scanner(content):
    result_tokens = []

    def on_match(result, index):
        nonlocal result_tokens

        list_of_lengths = []
        for machine_index in result:
            if machines[machine_index]['token']['type'] == 'function':
                list_of_lengths.append(len(result[machine_index]) - 1)
            else:
                list_of_lengths.append(len(result[machine_index]))

        highest_length = max(list_of_lengths)
        filter_by_len = list(filter(
            lambda item: len(item[1]) == highest_length,
            result.items()
        ))
        sorted_by_priority = list(sorted(
            filter_by_len,
            key=lambda item: machines[item[0]]['priority'],
            reverse=True
        ))


        candidate = sorted_by_priority[0]
        function_has_matched = list(filter(
            lambda item: machines[item[0]]['token']['type'] == 'function',
            result.items()
        ))
        if machines[candidate[0]]['token']['type'] == 'variable' and len(function_has_matched):
            candidate = function_has_matched[0]


        [machine_index, matched_string] = candidate
        token = machines[machine_index]['token']

        if token['type'] == 'function':
            result_tokens.append({"type": "function", "value": matched_string[0:-1]})
            result_tokens.append({"type": "par", "value": "("})
        elif token['type'] == 'delimiter':
            result_tokens.append({"type": "delimiter", "value": ";"})
        else:
            result_tokens.append({**token, "value": matched_string})

        return len(matched_string)

    MultiDFARunner.run(
        [machine['dfa'] for machine in machines],
        content,
        on_match
    )

    return result_tokens

