from compiler.project2.scanner import scanner
from compiler.project2.parser import parser
from compiler.project2.executer import executer

tokens = scanner("""
num := 4;
fact := 1;

while(num){
    fact := fact * num;
    num := num - 1;
}

print(fact)
""")

tokens = scanner("""

num := 10;

if(num - 10){
    num := 1;
}

print(num)

""")

actions = parser(tokens)
result = executer(actions)

# print('vars', result.vars)
# print('temp', result.temp)
# print('stack', result.stack)
#
print('code')
for i, code in enumerate(result.code):
    print(i, code)