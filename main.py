from Lexer import Lexer
from Parser import Parser

USER_INPUT = False
FILE_INPUT = True
SHOW_LEX = False
DEBUG = True

text = 'let a = 3; let b = 2; if false {print(a ^ b * 2 ^ 3 ^ 2);} else{print(a);}'

if USER_INPUT:
    text = input("Enter code: ")

if FILE_INPUT:
    f = open('test.ma', 'r')
    text = f.read()
    f.close()

lexer = Lexer()
lexer.build()

if SHOW_LEX:
    lexer.test(text)

parser = Parser().build()
ast = parser.parse(text, debug=DEBUG)

print("\nCode to execute:\n"+text)
print()

ast.eval()
