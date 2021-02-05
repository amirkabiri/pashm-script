from compiler.project2.scanner import scanner
from compiler.project2.parser import parser
from compiler.project2.executer import executer


def code(address):
    try:
        content = open(address).read()
    except:
        raise Exception('file address is invalid')

    tokens = scanner(content)
    actions = parser(tokens)

    result = ''
    for i, code in enumerate(actions.code):
        result += str(i) + '  ( '
        for i, item in enumerate(code):
            if isinstance(item, list):
                result += ':'.join([str(i) for i in item])
            if isinstance(item ,str):
                result += item

            if i != len(code) - 1:
                result += ' , '
        result += ' ) \n'

    return result


def run(address):
    try:
        content = open(address).read()
    except:
        raise Exception('file address is invalid')

    tokens = scanner(content)
    actions = parser(tokens)

    return executer(actions)