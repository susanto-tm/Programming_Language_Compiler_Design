from Lexer import Lexer
from Parser import Parser
# from Compiler import AST

lexer = Lexer()
lexer.build()
# lexer.test("let a = 2; print(a);")
parser = Parser().build()

for x in parser.parse("let a = 20; let x = 10; let c = a; c = 20; print(c*x--);"):
    x.compile()


