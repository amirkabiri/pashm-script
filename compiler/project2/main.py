from compiler.project2.scanner import scanner
from compiler.project2.parser import parser
from compiler.project2.executer import executer

tokens = scanner("b := 1 * (2 + 5)*5")
actions = parser(tokens)
result = executer(actions)

print('vars', result.vars)
print('temp', result.temp)


print('code')
for code in result.code:
    print(code)