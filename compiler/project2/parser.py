from compiler.grammar.grammar import Grammar
from compiler.grammar.expression import Variable, Terminal, Dollar, Action
from compiler.grammar.statement import Statement
from compiler.grammar.ll1 import LL1
from compiler.project2.code_generator import Actions


grammar = Grammar(
    [
        Variable('START'),
        Variable('STATEMENTS'),
        Variable('STATEMENTS1'),
        Variable('STATEMENT'),
        Variable('STATEMENT1'),
        Variable('FUNCTION_CALL_PARAMS'),
        Variable('FUNCTION_CALL_PARAMS1'),
        Variable('FUNCTION_CALL'),
        Variable('BLOCK'),
        Variable('TERM'),
        Variable('EXPRESSION'),
        Variable('MATH'),
        Variable('A'),
        Variable('A2'),
        Variable('A1'),
        Variable('B'),
        Variable('B2'),
        Variable('B1'),
        Variable('C'),
        Variable('D'),
        Variable('D1'),
        Variable('E'),
    ],
    [
        Terminal('function'),
        Terminal('delimiter'),
        Terminal('if'),
        Terminal('else'),
        Terminal('while'),
        Terminal('('),
        Terminal(')'),
        Terminal('do'),
        Terminal('variable'),
        Terminal(':='),
        Terminal('params_delimiter'),
        Terminal('{'),
        Terminal('}'),
        Terminal('number'),
        Terminal('+'),
        Terminal('*'),
        Terminal('/'),
        Terminal('-'),
        Terminal('^'),
    ],
    Variable('START'),
    [
        [Variable('START'), Statement([Variable('STATEMENTS')])],

        [Variable('STATEMENTS'), Statement([Variable('STATEMENT'), Variable('STATEMENTS1')])],
        [Variable('STATEMENTS'), Statement([Terminal('')])],
        # [Variable('STATEMENTS1'), Statement([Terminal('delimiter'), Variable('STATEMENTS')])],
        [Variable('STATEMENTS1'), Statement([Terminal('')])],

        [Variable('STATEMENT'), Statement([Terminal('if'), Terminal('('), Variable('EXPRESSION'), Action('save'), Terminal(')'), Variable('BLOCK'), Action('if'), Variable('STATEMENT1')])],
        [Variable('STATEMENT1'), Statement([Terminal('')])],
        [Variable('STATEMENT1'), Statement([Action('save'), Terminal('else'), Variable('BLOCK'), Action('else')])],

        [Variable('STATEMENT'), Statement([Terminal('while'), Terminal('('), Variable('EXPRESSION'), Action('save'), Terminal(')'), Variable('BLOCK'), Action('while')])],
        [Variable('STATEMENT'), Statement([Terminal('do'), Variable('BLOCK'), Terminal('while'), Terminal('('), Variable('EXPRESSION'), Action('do_while'), Terminal(')')])],
        [Variable('STATEMENT'), Statement([Terminal('variable'), Terminal(':='), Variable('MATH'), Action('assign')])],
        [Variable('STATEMENT'), Statement([Variable('FUNCTION_CALL')])],

        [Variable('FUNCTION_CALL'), Statement([Action('function'), Terminal('function'), Terminal('('), Variable('FUNCTION_CALL_PARAMS'), Terminal(')'), Action('call')])],
        [Variable('FUNCTION_CALL_PARAMS'), Statement([Variable('TERM'), Variable('FUNCTION_CALL_PARAMS1')])],
        [Variable('FUNCTION_CALL_PARAMS'), Statement([Terminal('')])],
        [Variable('FUNCTION_CALL_PARAMS1'), Statement([Terminal('params_delimiter'), Variable('FUNCTION_CALL_PARAMS')])],
        [Variable('FUNCTION_CALL_PARAMS1'), Statement([Terminal('')])],

        [Variable('BLOCK'), Statement([Variable('STATEMENT')])],
        [Variable('BLOCK'), Statement([Terminal('{'), Variable('STATEMENTS'), Terminal('}')])],

        [Variable('TERM'), Statement([Action('variable'), Terminal('variable')])],
        [Variable('TERM'), Statement([Action('number'), Terminal('number')])],

        [Variable('EXPRESSION'), Statement([Variable('MATH')])],

        [Variable('MATH'), Statement([Variable('A')])],

        [Variable('A'), Statement([Variable('B'), Variable('A2')])],
        [Variable('A2'), Statement([Variable('A1'), Variable('A2')])],
        [Variable('A2'), Statement([Terminal('')])],
        [Variable('A1'), Statement([Terminal('+'), Variable('B'), Action('add')])],
        [Variable('A1'), Statement([Terminal('-'), Variable('B'), Action('minus')])],

        [Variable('B'), Statement([Variable('C'), Variable('B2')])],
        [Variable('B2'), Statement([Variable('B1'), Variable('B2')])],
        [Variable('B2'), Statement([Terminal('')])],
        [Variable('B1'), Statement([Terminal('*'), Variable('C'), Action('multiply')])],
        [Variable('B1'), Statement([Terminal('/'), Variable('C'), Action('divide')])],

        [Variable('C'), Statement([Terminal('-'), Variable('C'), Action('invert')])],
        [Variable('C'), Statement([Variable('D')])],

        [Variable('D'), Statement([Variable('E'), Variable('D1')])],
        [Variable('D1'), Statement([Terminal('^'), Variable('D'), Action('pow')])],
        [Variable('D1'), Statement([Terminal('')])],

        [Variable('E'), Statement([Variable('TERM')])],
        [Variable('E'), Statement([Terminal('('), Variable('MATH'), Terminal(')')])],
    ]
)

grammar = Grammar(
    [
        Variable('START'), Variable('STATEMENTS'), Variable('STATEMENT'),
        Variable('BLOCK'), Variable('TERM'), Variable('EXPRESSION'),

        Variable('A'), Variable('A2'), Variable('A1'),
        Variable('B'), Variable('B2'), Variable('B1'),
        Variable('C'), Variable('D'), Variable('D1'),
        Variable('E'), Variable('MATH'),

        Variable('FUNCTION_CALL'), Variable('FUNCTION_CALL_PARAMS'), Variable('FUNCTION_CALL_PARAMS1'),
    ],
    [
        Terminal('if'), Terminal('('), Terminal(')'),
        Terminal('do'), Terminal('while'), Terminal(':='),
        Terminal('delimiter'), Terminal('{'), Terminal('}'),
        Terminal('variable'), Terminal('number'),

        Terminal('+'), Terminal('*'), Terminal('/'),
        Terminal('-'), Terminal('^'),

        Terminal('function'), Terminal('params_delimiter'),
    ],
    Variable("START"),
    [
        [Variable('START'), Statement([Variable('STATEMENTS')])],
        [Variable('STATEMENTS'), Statement([Variable('STATEMENT'), Variable('STATEMENTS')])],
        [Variable('STATEMENTS'), Statement([Terminal('')])],
        [Variable('STATEMENT'), Statement([Terminal('if'), Terminal('('), Variable('EXPRESSION'), Action('save'), Terminal(')'), Variable('BLOCK'), Action('if')])],
        [Variable('STATEMENT'), Statement([Terminal('while'), Terminal('('), Action('label'), Variable('EXPRESSION'), Action('save'), Terminal(')'), Variable('BLOCK'), Action('while')])],
        [Variable('STATEMENT'), Statement([Terminal('do'), Action('label'), Variable('BLOCK'), Terminal('while'), Terminal('('), Variable('EXPRESSION'), Action('do_while'), Terminal(')') ])],
        [Variable('STATEMENT'), Statement([Action('variable'), Terminal('variable'), Terminal(':='), Variable('EXPRESSION'), Action('assign'), Terminal('delimiter')])],
        [Variable('BLOCK'), Statement([Variable('STATEMENT')])],
        [Variable('BLOCK'), Statement([Terminal('{'), Variable('STATEMENTS'), Terminal('}')])],
        [Variable('TERM'), Statement([Action('variable'), Terminal('variable')])],
        [Variable('TERM'), Statement([Action('number'), Terminal('number')])],
        [Variable('EXPRESSION'), Statement([Variable('MATH')])],

        [Variable('MATH'), Statement([Variable('A')])],
        [Variable('A'), Statement([Variable('B'), Variable('A2')])],
        [Variable('A2'), Statement([Variable('A1'), Variable('A2')])],
        [Variable('A2'), Statement([Terminal('')])],
        [Variable('A1'), Statement([Terminal('+'), Variable('B'), Action('add')])],
        [Variable('A1'), Statement([Terminal('-'), Variable('B'), Action('minus')])],
        [Variable('B'), Statement([Variable('C'), Variable('B2')])],
        [Variable('B2'), Statement([Variable('B1'), Variable('B2')])],
        [Variable('B2'), Statement([Terminal('')])],
        [Variable('B1'), Statement([Terminal('*'), Variable('C'), Action('multiply')])],
        [Variable('B1'), Statement([Terminal('/'), Variable('C'), Action('divide')])],
        [Variable('C'), Statement([Terminal('-'), Variable('C'), Action('invert')])],
        [Variable('C'), Statement([Variable('D')])],
        [Variable('D'), Statement([Variable('E'), Variable('D1')])],
        [Variable('D1'), Statement([Terminal('^'), Variable('D'), Action('pow')])],
        [Variable('D1'), Statement([Terminal('')])],
        [Variable('E'), Statement([Variable('TERM')])],
        [Variable('E'), Statement([Terminal('('), Variable('MATH'), Terminal(')')])],


        [Variable('STATEMENT'), Statement([Variable('FUNCTION_CALL')])],
        [Variable('FUNCTION_CALL'), Statement([Action('function'), Terminal('function'), Terminal('('), Variable('FUNCTION_CALL_PARAMS'), Terminal(')'), Action('call')])],
        [Variable('FUNCTION_CALL_PARAMS'), Statement([Variable('TERM'), Variable('FUNCTION_CALL_PARAMS1')])],
        [Variable('FUNCTION_CALL_PARAMS1'), Statement([Terminal('params_delimiter'), Variable('FUNCTION_CALL_PARAMS')])],
        [Variable('FUNCTION_CALL_PARAMS1'), Statement([Terminal('')])],
        [Variable('FUNCTION_CALL_PARAMS'), Statement([Terminal('')])],

    ]
)


def get_token_nickname(token):
    if token['type'] in ['operator', 'par', 'brace', 'end']:
        return token['value']

    return token["type"]


def parser(tokens):
    ll1 = LL1(grammar, {
        'START': [Dollar()],
        'STATEMENTS': [Dollar(), Terminal('}')],
        'STATEMENT': [Terminal('while'), Dollar(), Terminal('}'), Terminal('if'), Terminal('while'), Terminal('do'), Terminal('variable')],
        'BLOCK': [Terminal('while'), Dollar(), Terminal('}'), Terminal('if'), Terminal('while'), Terminal('do'), Terminal('variable')],
        'TERM': [Terminal('^'), Terminal('*'), Terminal('/'), Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'EXPRESSION': [Terminal(')')],

        'A': [Terminal('delimiter'), Terminal(')')],
        'A2': [Terminal('delimiter'), Terminal(')')],
        'A1': [Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'B': [Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'B2': [Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'B1': [Terminal('*'), Terminal('/'), Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'C': [Terminal('*'), Terminal('/'), Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'D': [Terminal('*'), Terminal('/'), Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'D1': [Terminal('*'), Terminal('/'), Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'E': [Terminal('^'), Terminal('*'), Terminal('/'), Terminal('+'), Terminal('-'), Terminal('delimiter'), Terminal(')')],
        'MATH': [Terminal('delimiter'), Terminal(')')],

        'FUNCTION_CALL': [Terminal('while'), Dollar(), Terminal('}'), Terminal('if'), Terminal('while'), Terminal('do'), Terminal('variable')],
        'FUNCTION_CALL_PARAMS': [Terminal(')')],
        'FUNCTION_CALL_PARAMS1': [Terminal(')')],
    })
    tokens = [{ "type": "end", "value": "$" }, *(tokens[::-1])]
    stack = [Dollar(), grammar.start]
    actions = Actions()

    while len(tokens) > 1 or len(stack) > 1:
        # print(f'---------------------')
        # print('stack', stack)
        # print('tokens', [token['type'] for token in tokens])

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
            # print('action: ', head.value)
            getattr(actions, 'action_' + head.value[1:])(token)

    if stack[0].value == tokens[0]['value'] and stack[0].is_dollar():
        return actions
    else:
        raise Exception("SyntaxError: I don't know where, but you have syntax error!")