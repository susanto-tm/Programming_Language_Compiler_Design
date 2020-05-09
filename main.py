from Lexer import Lexer
from Parser import Parser

USER_INPUT = False
SHOW_LEX = False
DEBUG = True

text = 'let a = 2 + 2;print(a and 0);'

if USER_INPUT:
    text = input("Enter code: ")

lexer = Lexer()
lexer.build()

if SHOW_LEX:
    lexer.test(text)

parser = Parser().build()
ast = parser.parse(text, debug=DEBUG)
ast.eval()