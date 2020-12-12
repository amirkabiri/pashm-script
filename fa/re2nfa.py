from compiler.grammar import Grammar
from compiler.expression import Variable, Terminal, Dollar
from compiler.statement import Statement
from json import dumps
from compiler.helpers import unique_expressions

def tokenizer(regex):
    tokens = []

    for chr in regex:
        if chr in ('(', ')'):
            tokens.append({ 'type': 'par', 'value': chr })
            continue

        if chr == '*':
            tokens.append({'type': 'star', 'value': chr})
            continue

        if chr == '+':
            tokens.append({'type': 'plus', 'value': chr})
            continue

        if chr == '|':
            tokens.append({'type': 'union', 'value': chr})
            continue

        tokens.append({'type': 'char', 'value': chr})

    return tokens


class LL1:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.first = self.fill_first()
        self.follow = self.fill_follow()
        self.table = self.fill_table()

    def fill_table(self):
        table = dict(map(
            lambda variable: [
                variable.value,
                dict(map(
                    lambda expr : [expr.value, None],
                    self.grammar.terminals + [Dollar()]
                ))
            ],
            self.grammar.variables
        ))

        for i, [variable, statement] in enumerate(self.grammar.productions):
            first = [statement[0]]
            if isinstance(statement[0], Variable):
                first = self.first[statement[0].value]

            has_lambda = False

            for terminal in first:
                if terminal.is_lambda():
                    has_lambda = True
                    continue

                if table[variable.value][terminal.value] != None:
                    raise Exception('this grammar is not in LL1 form')

                table[variable.value][terminal.value] = i + 1

            if has_lambda:
                follow = self.follow[variable.value]

                for expr in follow:
                    table[variable.value][expr.value] = i + 1

        return table

    def fill_follow(self):
        grammar = self.grammar
        follow = dict(map(
            lambda variable: [variable.value, []],
            grammar.variables
        ))

        for variable in self.grammar.variables:
            follow[variable.value] = self.find_follow(variable)

        # removing duplicate expressions from follows
        for var in follow:
            follow[var] = unique_expressions(follow[var])

        return follow

    def find_follow(self, target: Variable) -> list:
        follow = []

        if self.grammar.start == target:
            follow.append(Dollar())

        for variable, statement in self.grammar.productions:
            for i, expr in enumerate(statement):
                if expr != target:
                    continue

                # if expr is last expression of statement
                if len(statement[i+1:]) == 0:
                    if variable != target:
                        # add variable follow to it, example: A -> aB
                        follow = follow + self.find_follow(variable)
                    continue

                next_expr = statement[i+1]
                if isinstance(next_expr, Terminal):
                    first = [next_expr]
                else:
                    first = self.first[next_expr.value]


                first_has_lambda = any(terminal.is_lambda() for terminal in first)

                follow = follow + list(filter(
                    lambda terminal: not terminal.is_lambda(),
                    first
                ))

                if first_has_lambda:
                    follow = follow + self.find_follow(variable)

        return follow

    def fill_first(self):
        first = dict(map(
            lambda variable: [variable.value, []],
            self.grammar.variables
        ))

        for [variable, statement] in self.grammar.productions:
            statement_first = self.find_first(statement)
            first[variable.value] = [
                *first[variable.value],
                *statement_first
            ]

        # removing duplicate expressions from firsts
        for var in first:
            first[var] = unique_expressions(first[var])

        return first

    def find_first(self, statement: Statement):
        if isinstance(statement[0], Terminal):
            return statement[0:1]

        i = 0
        first = []
        while i < len(statement):
            if isinstance(statement[i], Terminal):
                return first

            var_statements = self.grammar[statement[i].value]
            var_first = []
            for var_statement in var_statements:
                var_first = var_first + self.find_first(var_statement)

            var_first_has_lambda = any(terminal.is_lambda() for terminal in var_first)

            if not var_first_has_lambda:
                return var_first

            first = first + list(filter(lambda terminal: not terminal.is_lambda(), var_first))

            i += 1

        return first


def parser(tokens):
    grammar = Grammar(
        [
            Variable('A'), Variable("A'"), Variable('B'), Variable("B'"),
            Variable('C'), Variable("C'"), Variable('D'),
        ],[
            Terminal('|'), Terminal('.'), Terminal('*'), Terminal('+'),
            Terminal('('), Terminal(')'), Terminal('id'),
        ],
        Variable('A'),
        [
            [Variable('A'), Statement([Variable('B'), Variable("A'")])],

            [Variable("A'"), Statement([Terminal('')])],
            [Variable("A'"), Statement([Terminal('|'), Variable('B'), Variable("A'")])],

            [Variable("B"), Statement([Variable('C'), Variable("B'")])],
            [Variable("B'"), Statement([Terminal('.'), Variable('C'), Variable("B'")])],
            [Variable("B'"), Statement([Terminal('')])],

            [Variable("C"), Statement([Variable('D'), Variable("C'")])],
            [Variable("C'"), Statement([Terminal('+')])],
            [Variable("C'"), Statement([Terminal('*')])],
            [Variable("C'"), Statement([Terminal('')])],

            [Variable("D"), Statement([Terminal('id')])],
            [Variable("D"), Statement([Terminal('('), Variable('A'), Terminal(')')])],
        ]
    )
    grammar = Grammar(
        [Variable('A'), Variable('B')],
        [Terminal('a'), Terminal('b'), Terminal('f')],
        Variable('A'),
        [
            [Variable('A'), Statement([Variable('A'), Terminal('a'), Variable('B')])],
            [Variable('A'), Statement([Variable('A'), Terminal('b'), Variable('B')])],
            [Variable('B'), Statement([Terminal('')])],
            [Variable('B'), Statement([Terminal('f'), Variable('B')])],
            [Variable('A'), Statement([Terminal('')])],
        ]
    )
    # print(grammar)
    # print()

    i = 0
    l = LL1(grammar)

    print('first')
    for e in l.first:
        print(e)
    print()

    print('follow')
    for e in l.follow:
        print(e)

    def run_var(variable: Variable):
        nonlocal i
        for statement in grammar[variable.value]:
            first = [statement[0]]
            if isinstance(statement[0], Variable):
                first = l.first[statement[0].value]

            for terminal in first:
                if terminal.value == 'id' and tokens[i]['type'] == 'char' or terminal.value == tokens[i]['value']:
                    result = []
                    for expr in grammar.productions[l.table[variable.value][terminal.value]][1]:
                        if isinstance(expr, Terminal):
                            result.append(run_terminal(expr))
                        else:
                            result.append(run_var(expr))
                    return result

        raise Exception('syntax error in run_var')


    def run_terminal(terminal: Terminal):
        nonlocal i
        if terminal.value == 'id' and tokens[i]['type'] == 'char' or terminal.value == tokens[i]['value']:
            i += 1
            return i
        else:
            raise Exception('syntax error in run_terminal', terminal, tokens[i]['value'])

    return 'hi'
    return run_var(grammar.start)


tokens = tokenizer('a+b')
print(tokens)

print()

ast = parser(tokens)
# print(ast)

# l = LL1(grammar)
#
# print('firsts')
# for var in l.follow:
#     print(var, l.follow[var])
#
# print()
#
# print('follows')
# for var in l.first:
#     print(var, l.first[var])
#
# print()
#
# print('LL1 table')
# for var in l.table:
#     print(var, l.table[var])

# s = Statement([Terminal('a'), Variable('A')])
# print(len(s))
