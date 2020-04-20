from Lexer import Lexer
from Parser import Parser
# from Compiler import AST

lexer = Lexer()
lexer.build()
# lexer.test("let a = 2; print(a);")
parser = Parser().build()

for x in parser.parse("let a = 2; print(a); a = 3; print(a);"):
    x.compile()


