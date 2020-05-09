import ply.yacc as yacc
from Lexer import Lexer
from Compiler import *
import ast

class Parser:
    tokens = Lexer.tokens
    precedence = (
        ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('right', 'POW'),
        # ('right', 'NEGATE')
    )

    def p_program(self, p):
        """
        program : line_statement
        """
        p[0] = Program(p[1]).eval()

    def p_assignment(self, p):
        """
        line_statement : LET IDENTIFIER EQUALS expression SEMICOLON
        """
        p[0] = Assign(Identifier(p[2], 'store').eval(), p[4]).eval()

    def p_print_statement(self, p):
        """
        line_statement : line_statement statement SEMICOLON
                       | empty
        """
        if len(p) > 2:
            p[0] = [p[1]]
            p[0].append(Expression(p[2]))

    def p_PRINT(self, p):
        """
        statement : PRINT LPAREN expression RPAREN
        """
        p[0] = FuncCall(PrintStmt(), p[3])

    def p_expr_identifier(self, p):
        """
        expression : IDENTIFIER
        """
        p[0] = Identifier(p[1], 'load').eval()

    def p_expr_INTCONST(self, p):
        """
        expression : INTCONST
        """
        p[0] = Constant(int(p[1])).eval()

    def p_expr_FLOATCONST(self, p):
        """
        expression : FLOATCONST
        """
        p[0] = Constant(float(p[1])).eval()

    def p_expr_STRINGCONST(self, p):
        """
        expression : STRINGCONST
        """
        p[0] = Constant(str(p[1])).eval()

    def p_empty(self, p):
        """
        empty :
        """
        pass

    def p_error(self, p):
        pass

    def build(self):
        self.parser = yacc.yacc(module=self)
        return self.parser

