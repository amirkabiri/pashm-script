from compiler.project2.scanner import scanner
from compiler.project2.parser import parser
from compiler.project2.executer import executer
from sys import argv


content = ""
try:
    content = open(argv[2]).read()
except:
    print('Pashmam: file address is invalid')
    exit()


actions = None
try:
    tokens = scanner(content)
    actions = parser(tokens)
except Exception as e:
    print('Pashmam: ' + str(e))
    exit()


if argv[1] == 'run':
    try:
        executer(actions)
    except Exception as e:
        print('Pashmam: ' + str(e))
elif argv[1] == 'code':
    for i, code in enumerate(actions.code):
        print(i, end='  ( ')
        for i, item in enumerate(code):
            if isinstance(item, list):
                print(':'.join([str(i) for i in item]), end='')
            if isinstance(item ,str):
                print(item, end='')

            if i != len(code) - 1:
                print(end=' , ')
        print(' ) ')