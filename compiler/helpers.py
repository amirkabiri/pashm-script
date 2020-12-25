from typing import List
from compiler.grammar.expression import Expression


def unique_expressions(expressions: List[Expression]):
    result = []

    for expr in expressions:
        exists = any(e == expr for e in result)

        if not exists:
            result.append(expr)

    return result
