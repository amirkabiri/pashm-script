from compiler.grammar.grammar import Grammar
from compiler.grammar.expression import Variable, Terminal, Dollar, Action
from compiler.grammar.statement import Statement
from compiler.grammar.ll1 import LL1
from compiler.project2.code_generator import Actions


grammar = Grammar(
    [Variable("S"), Variable("E"), Variable("E'"), Variable("T"), Variable("T'"), Variable("F"), Variable("L")],
    [Terminal(':='), Terminal('*'), Terminal('+'), Terminal('('), Terminal(')'), Terminal('variable'), Terminal('number')],
    Variable('S'),
    [
        [Variable("S"), Statement([Variable("L"), Terminal(":="), Variable("E"), Action('assign')])],
        [Variable("E"), Statement([Variable("T"), Variable("E'")])],
        [Variable("E'"), Statement([Terminal("")])],
        [Variable("E'"), Statement([Terminal("+"), Variable("T"), Action('add'), Variable("E'")])],
        [Variable("T"), Statement([Variable("F"), Variable("T'")])],
        [Variable("T'"), Statement([Terminal("")])],
        [Variable("T'"), Statement([Terminal("*"), Variable("F"), Action('mult'), Variable("T'")])],
        [Variable("F"), Statement([Terminal("("), Variable("E"), Terminal(")")])],
        [Variable("F"), Statement([Action('number'), Terminal("number")])],
        [Variable("L"), Statement([Action('variable'), Terminal("variable")])],
    ]
)


def get_token_nickname(token):
    if token["type"] == "operator" or token["type"] == "par":
        return token["value"]

    if token["type"] == "end":
        return token["value"]

    return token["type"]


def parser(tokens):
    ll1 = LL1(grammar)
    tokens = [{ "type": "end", "value": "$" }, *(tokens[::-1])]
    stack = [Dollar(), grammar.start]
    actions = Actions()

    while len(tokens) > 1 or len(stack) > 1:
        head = stack.pop()
        token = tokens[-1]

        if isinstance(head, Variable):
            target = ll1.table[head.value][get_token_nickname(token)]

            if target is None:
                raise Exception("SyntaxError: I don't know where, but you have syntax error!")

            statement = grammar.productions[target][1].value[::-1]
            stack = stack + list(filter(
                lambda x: not x.is_lambda(),
                statement
            ))
        elif isinstance(head, Terminal):
            if head.value == get_token_nickname(token):
                tokens.pop()
            else:
                raise Exception("SyntaxError: I don't know where, but you have syntax error!")
        elif isinstance(head, Action):
            getattr(actions, 'action_' + head.value[1:])(token)

    if stack[0].value == tokens[0]['value'] and stack[0].is_dollar():
        return actions
    else:
        raise Exception("SyntaxError: I don't know where, but you have syntax error!")