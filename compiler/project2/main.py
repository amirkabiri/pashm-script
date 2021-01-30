from compiler.project2.scanner import scanner
from compiler.project2.parser import parser
from compiler.project2.executer import executer

tokens = scanner("""
b := 1;
a := 2;

while(a){
    b := b + 1;
    a := a - 1;
}
""")
# for token in tokens:
#     print(token)

actions = parser(tokens)
result = executer(actions)

print('vars', result.vars)
print('temp', result.temp)
print('stack', result.stack)

print('code')
for i, code in enumerate(result.code):
    print(i, code)