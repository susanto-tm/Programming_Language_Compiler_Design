from Lexer import Lexer
from Parser import Parser
# from Compiler import AST

lexer = Lexer()
lexer.build()
lexer.test("let a = 5; let x = 200; let c = a; print(c);")
# lexer.test("let a = 2; print(a);")
parser = Parser().build()

for x in parser.parse("let a = 5; let x = 200; let c = a; c = 500; print(c+x);"):
    x.compile()


