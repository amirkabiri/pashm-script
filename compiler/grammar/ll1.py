from compiler.grammar.grammar import Grammar
from compiler.grammar.expression import Variable, Terminal, Dollar, Action
from compiler.grammar.statement import Statement
from compiler.helpers import unique_expressions


class LL1:
    def __init__(self, grammar: Grammar):
        productions = []
        for production in grammar.productions:
            productions.append([
                production[0],
                Statement(list(filter(
                    lambda expr: isinstance(expr, Terminal) or isinstance(expr, Variable),
                    production[1].value
                )))
            ])
        self.grammar = Grammar(
            grammar.variables,
            grammar.terminals,
            grammar.start,
            productions
        )

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

                table[variable.value][terminal.value] = i

            if has_lambda:
                follow = self.follow[variable.value]

                for expr in follow:
                    table[variable.value][expr.value] = i

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
