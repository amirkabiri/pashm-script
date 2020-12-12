from compiler.expression import Variable, Terminal
from compiler.statement import Statement
from compiler.statements import Statements


class Grammar:
    def __init__(self, variables: list, terminals: list, start: Variable, productions):
        if not isinstance(variables, list) or any(not isinstance(variable, Variable) for variable in variables):
            raise TypeError('variables must be list of Variable objects')

        if not isinstance(terminals, list) or any(not isinstance(terminal, Terminal) for terminal in terminals):
            raise TypeError('terminals must be list of Terminal objects')

        if not isinstance(start, Variable):
            raise TypeError('start must be instance of Variable')

        self.start = start
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.value = self.create_value()

    def create_value(self):
        value = dict(map(
            lambda variable: [
                variable.value,
                Statements([])
            ],
            self.variables
        ))

        for [variable, statement] in self.productions:
            value[variable.value] = value[variable.value] + statement

        return value


    def __getitem__(self, key):
        return self.value[key]

    def __repr__(self):
        return "\n".join(map(
            lambda item: str(item[0]) + ' -> ' + str(item[1]),
            self.value.items()
        ))


# class LL1:
#     def __init__(self, grammar):
#         pass
#
# def first(grammar):
#     first = dict(map(
#         lambda variable: [variable.value, []],
#         grammar.variables
#     ))
#
#     for variable in grammar.value:
#         for statement in grammar.value[variable]:
#             pass
#
#
# g = Grammar(
#     [Variable('A'), Variable('B')],
#     [Terminal('a'), Terminal('b'), Terminal('c')],
#     Variable('A'),
#     [
#         [
#             Variable('A'),
#             Statement([Terminal('a'), Variable('A')])
#         ],
#         [
#             Variable('A'),
#             Statement([Terminal('c'), Variable('B')])
#         ],
#         [
#             Variable('B'),
#             Statement([Terminal('b'), Variable('B')])
#         ],
#         [
#             Variable('B'),
#             Statement([Terminal('b')])
#         ],
#     ]
# )
#
#
# regexGrammar = Grammar(
#     [Variable('A'), Variable('B'), Variable('C'), Variable('D'), ],
#     [Terminal('|'), Terminal('.'), Terminal('*'), Terminal('+'), Terminal('('), Terminal(')'), Terminal('id'), ],
#     Variable('A'),
#     [
#         [
#             Variable('A'),
#             Statement([Variable('A'), Terminal('|'), Variable('B')])
#         ],
#         [
#             Variable('A'),
#             Statement([Variable('B')])
#         ],
#         [
#             Variable('B'),
#             Statement([Variable('B'), Terminal('.'), Variable('C')])
#         ],
#         [
#             Variable('B'),
#             Statement([Variable('C')])
#         ],
#         [
#             Variable('C'),
#             Statement([Variable('D'), Terminal('*')])
#         ],
#         [
#             Variable('C'),
#             Statement([Variable('D'), Terminal('+')])
#         ],
#         [
#             Variable('C'),
#             Statement([Variable('D')])
#         ],
#         [
#             Variable('D'),
#             Statement([Terminal('id')])
#         ],
#         [
#             Variable('D'),
#             Statement([Terminal('('), Variable('A'), Terminal(')')])
#         ],
#     ]
# )
#
# l = LL1(regexGrammar)
# print(regexGrammar)
# print(l.first)