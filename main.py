from compiler.project2.main import run, code
from sys import argv

try:
    if argv[1] == 'run':
        run(argv[2])
    elif argv[1] == 'code':
        print(code(argv[2]), end='')
except Exception as e:
    print('Pashmam: ' + str(e))