from compiler.grammar.grammar import Grammar
from compiler.grammar.expression import Variable, Terminal, Dollar, Action
from compiler.grammar.statement import Statement
from compiler.grammar.ll1 import LL1
from compiler.project2.code_generator import Actions

grammar = Grammar(
    [
        Variable('START'),
        Variable('STATEMENTS'),
        Variable('STATEMENT'),
        # Variable('IF'),
        Variable('FUNCTION_CALL'),
        Variable('FUNCTION_CALL_PARAMS'),
        Variable('FUNCTION_CALL_PARAMS1'),
        Variable('BLOCK'),
        Variable('TERM'),
        Variable('EXPRESSION'),
        Variable('A'),
        Variable('A2'),
        Variable('B'),
        Variable('B2'),
        Variable('C'),
        Variable('C2'),
        Variable('C1'),
        Variable('D'),
        Variable('D2'),
        Variable('D1'),
        Variable('E'),
        Variable('E2'),
        Variable('E1'),
        Variable('F'),
        Variable('F2'),
        Variable('F1'),
        Variable('G'),
        Variable('G1'),
        Variable('H'),
        Variable('I'),
        Variable('VOID_FUNCTION_CALL'),
    ],
    [
        Terminal('while'),
        Terminal('('),
        Terminal(')'),
        Terminal('do'),
        Terminal('variable'),
        Terminal(':='),
        Terminal('delimiter'),
        Terminal('if'),
        # Terminal('else'),
        Terminal('function'),
        Terminal('params_delimiter'),
        Terminal('{'),
        Terminal('}'),
        Terminal('number'),
        Terminal('||'),
        Terminal('&&'),
        Terminal('!='),
        Terminal('=='),
        Terminal('>='),
        Terminal('>'),
        Terminal('<='),
        Terminal('<'),
        Terminal('-'),
        Terminal('+'),
        Terminal('*'),
        Terminal('/'),
        Terminal('%'),
        Terminal('^'),
        Terminal('!'),
    ],
    Variable("START"),
    [
        [Variable('START'), Statement([Variable('STATEMENTS')])],
        [Variable('STATEMENTS'), Statement([Variable('STATEMENT'), Variable('STATEMENTS')])],
        [Variable('STATEMENTS'), Statement([Terminal('')])],
        [Variable('STATEMENT'), Statement([Terminal('while'), Terminal('('), Action('label'), Variable('EXPRESSION'), Action('save'), Terminal(')'), Variable('BLOCK'), Action('while')])],
        [Variable('STATEMENT'), Statement([Terminal('do'), Variable('BLOCK'), Terminal('while'), Terminal('('), Variable('EXPRESSION'), Action('do_while'), Terminal(')')])],
        [Variable('STATEMENT'), Statement([Action('variable'), Terminal('variable'), Terminal(':='), Variable('EXPRESSION'), Terminal('delimiter'), Action('assign')])],
        [Variable('STATEMENT'), Statement([Variable('VOID_FUNCTION_CALL'), Terminal('delimiter')])],
        [Variable('STATEMENT'), Statement([Terminal('if'), Terminal('('), Variable('EXPRESSION'), Action('save'), Terminal(')'), Variable('BLOCK'), Action('if')])],
        # [Variable('STATEMENT'), Statement([Terminal('if'), Terminal('('), Variable('EXPRESSION'), Action('save'), Terminal(')'), Variable('BLOCK'), Action('if'), Variable('IF')])],
        # [Variable('IF'), Statement([Terminal('')])],
        # [Variable('IF'), Statement([Action('save'), Terminal('else'), Variable('BLOCK'), Action('else')])],
        [Variable('VOID_FUNCTION_CALL'), Statement([Action('function'), Terminal('function'), Terminal('('), Variable('FUNCTION_CALL_PARAMS'), Terminal(')'), Action('void_call')])],
        [Variable('FUNCTION_CALL'), Statement([Action('function'), Terminal('function'), Terminal('('), Variable('FUNCTION_CALL_PARAMS'), Terminal(')'), Action('call')])],
        [Variable('FUNCTION_CALL_PARAMS'), Statement([Variable('TERM'), Variable('FUNCTION_CALL_PARAMS1')])],
        [Variable('FUNCTION_CALL_PARAMS1'), Statement([Terminal('params_delimiter'), Variable('FUNCTION_CALL_PARAMS')])],
        [Variable('FUNCTION_CALL_PARAMS1'), Statement([Terminal('')])],
        [Variable('FUNCTION_CALL_PARAMS'), Statement([Terminal('')])],
        [Variable('BLOCK'), Statement([Variable('STATEMENT')])],
        [Variable('BLOCK'), Statement([Terminal('{'), Variable('STATEMENTS'), Terminal('}')])],
        [Variable('TERM'), Statement([Action('variable'), Terminal('variable')])],
        [Variable('TERM'), Statement([Action('number'), Terminal('number')])],
        [Variable('TERM'), Statement([Variable('FUNCTION_CALL')])],
        [Variable('EXPRESSION'), Statement([Variable('A')])],
        [Variable('A'), Statement([Variable('B'), Variable('A2')])],
        [Variable('A2'), Statement([Terminal('||'), Variable('B'), Action('or'), Variable('A2')])],
        [Variable('A2'), Statement([Terminal('')])],
        [Variable('B'), Statement([Variable('C'), Variable('B2')])],
        [Variable('B2'), Statement([Terminal('&&'), Variable('C'), Action('and'), Variable('B2')])],
        [Variable('B2'), Statement([Terminal('')])],
        [Variable('C'), Statement([Variable('D'), Variable('C2')])],
        [Variable('C2'), Statement([Variable('C1'), Variable('C2')])],
        [Variable('C2'), Statement([Terminal('')])],
        [Variable('C1'), Statement([Terminal('!='), Variable('D'), Action('not_equal')])],
        [Variable('C1'), Statement([Terminal('=='), Variable('D'), Action('equal')])],
        [Variable('D'), Statement([Variable('E'), Variable('D2')])],
        [Variable('D2'), Statement([Variable('D1'), Variable('D2')])],
        [Variable('D2'), Statement([Terminal('')])],
        [Variable('D1'), Statement([Terminal('>='), Variable('E'), Action('greater_than_and_equal')])],
        [Variable('D1'), Statement([Terminal('>'), Variable('E'), Action('greater_than')])],
        [Variable('D1'), Statement([Terminal('<='), Variable('E'), Action('less_than_and_equal')])],
        [Variable('D1'), Statement([Terminal('<'), Variable('E'), Action('less_than')])],
        [Variable('E'), Statement([Variable('F'), Variable('E2')])],
        [Variable('E2'), Statement([Variable('E1'), Variable('E2')])],
        [Variable('E2'), Statement([Terminal('')])],
        [Variable('E1'), Statement([Terminal('-'), Variable('F'), Action('subtract')])],
        [Variable('E1'), Statement([Terminal('+'), Variable('F'), Action('add')])],
        [Variable('F'), Statement([Variable('G'), Variable('F2')])],
        [Variable('F2'), Statement([Variable('F1'), Variable('F2')])],
        [Variable('F2'), Statement([Terminal('')])],
        [Variable('F1'), Statement([Terminal('*'), Variable('G'), Action('multiply')])],
        [Variable('F1'), Statement([Terminal('/'), Variable('G'), Action('divide')])],
        [Variable('F1'), Statement([Terminal('%'), Variable('G'), Action('modulo')])],
        [Variable('G'), Statement([Variable('H'), Variable('G1')])],
        [Variable('G1'), Statement([Terminal('^'), Variable('G'), Action('pow')])],
        [Variable('G1'), Statement([Terminal('')])],
        [Variable('H'), Statement([Terminal('-'), Variable('H'), Action('unary_minus')])],
        [Variable('H'), Statement([Terminal('+'), Variable('H'), Action('unary_plus')])],
        [Variable('H'), Statement([Terminal('!'), Variable('H'), Action('not')])],
        [Variable('H'), Statement([Variable('I')])],
        [Variable('I'), Statement([Variable('TERM')])],
        [Variable('I'), Statement([Terminal('('), Variable('EXPRESSION'), Terminal(')')])],
    ]
)


# print(grammar.export_for_node())
# exit()

def get_token_nickname(token):
    if token['type'] in ['operator', 'par', 'brace', 'end']:
        return token['value']

    return token["type"]


def parser(tokens):
    ll1 = LL1(
        grammar,
        {'START': [Dollar()], 'STATEMENTS': [Dollar(), Terminal('}')],
         'STATEMENT': [Terminal('while'), Terminal('do'), Terminal('variable'), Terminal('if'), Terminal('function'),
                       Dollar(), Terminal('}')],
         'FUNCTION_CALL': [Terminal('delimiter'), Terminal('params_delimiter'), Terminal(')'), Terminal('^'),
                           Terminal('*'), Terminal('/'), Terminal('%'), Terminal('-'), Terminal('+'), Terminal('>='),
                           Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='), Terminal('&&'),
                           Terminal('||')], 'FUNCTION_CALL_PARAMS': [Terminal(')')],
         'FUNCTION_CALL_PARAMS1': [Terminal(')')],
         'BLOCK': [Terminal('while'), Terminal('do'), Terminal('variable'), Terminal('if'), Terminal('function'),
                   Dollar(), Terminal('}')],
         'TERM': [Terminal('params_delimiter'), Terminal(')'), Terminal('^'), Terminal('*'), Terminal('/'),
                  Terminal('%'), Terminal('-'), Terminal('+'), Terminal('>='), Terminal('>'), Terminal('<='),
                  Terminal('<'), Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'), Terminal('delimiter')],
         'EXPRESSION': [Terminal(')'), Terminal('delimiter')], 'A': [Terminal(')'), Terminal('delimiter')],
         'A2': [Terminal(')'), Terminal('delimiter')], 'B': [Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'B2': [Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'C': [Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'C2': [Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'C1': [Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'D': [Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'D2': [Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'D1': [Terminal('>='), Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='),
                Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'E': [Terminal('>='), Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='),
               Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'E2': [Terminal('>='), Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='),
                Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'E1': [Terminal('-'), Terminal('+'), Terminal('>='), Terminal('>'), Terminal('<='), Terminal('<'),
                Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'F': [Terminal('-'), Terminal('+'), Terminal('>='), Terminal('>'), Terminal('<='), Terminal('<'),
               Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'F2': [Terminal('-'), Terminal('+'), Terminal('>='), Terminal('>'), Terminal('<='), Terminal('<'),
                Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'F1': [Terminal('*'), Terminal('/'), Terminal('%'), Terminal('-'), Terminal('+'), Terminal('>='),
                Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='), Terminal('&&'),
                Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'G': [Terminal('*'), Terminal('/'), Terminal('%'), Terminal('-'), Terminal('+'), Terminal('>='), Terminal('>'),
               Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='), Terminal('&&'), Terminal('||'),
               Terminal(')'), Terminal('delimiter')],
         'G1': [Terminal('*'), Terminal('/'), Terminal('%'), Terminal('-'), Terminal('+'), Terminal('>='),
                Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='), Terminal('&&'),
                Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'H': [Terminal('^'), Terminal('*'), Terminal('/'), Terminal('%'), Terminal('-'), Terminal('+'), Terminal('>='),
               Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='), Terminal('&&'),
               Terminal('||'), Terminal(')'), Terminal('delimiter')],
         'I': [Terminal('^'), Terminal('*'), Terminal('/'), Terminal('%'), Terminal('-'), Terminal('+'), Terminal('>='),
               Terminal('>'), Terminal('<='), Terminal('<'), Terminal('!='), Terminal('=='), Terminal('&&'),
               Terminal('||'), Terminal(')'), Terminal('delimiter')]}
    )
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
                raise Exception("I don't know where, but you have syntax error!")

            statement = grammar.productions[target][1].value[::-1]
            stack = stack + list(filter(
                lambda x: not x.is_lambda(),
                statement
            ))
        elif isinstance(head, Terminal):
            if head.value == get_token_nickname(token):
                tokens.pop()
            else:
                raise Exception("I don't know where, but you have syntax error!")
        elif isinstance(head, Action):
            getattr(actions, 'before')(head.value, token)
            getattr(actions, 'action_' + head.value[1:])(token)
            getattr(actions, 'after')(head.value, token)
            # print(head.value, actions.stack)

    if stack[0].value == tokens[0]['value'] and stack[0].is_dollar():
        return actions
    else:
        raise Exception("I don't know where, but you have syntax error!")