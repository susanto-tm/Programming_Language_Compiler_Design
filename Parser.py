import ply.yacc as yacc
from Lexer import Lexer
from Compiler import AST

DEBUG_MODE = False


class Parser:
    tokens = Lexer.tokens
    precedence = (
        # ('nonassoc', 'LOOP_INSTRUCT'),
        ('nonassoc', 'IF', 'FOR'),
        # ('left', 'CONDITION'),
        ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('right', 'POW'),
        ('right', 'NEGATE')
    )

    def p_line_statement(self, p):
        """
        line_statement : statement_list SEMICOLON
        """
        p[0] = p[1]

    def p_declaration(self, p):
        """
        decl_statement : LET IDENTIFIER EQUALS expression
                       | LET IDENTIFIER
        """
        if len(p) > 4:
            p[0] = AST(action='assign', params=[p[2], p[4]])
        else:
            debug("IDENTIFIER", p[2])
            p[0] = AST(action='assign', params=[p[2], 0])

    def p_decl_assign(self, p):
        """
        decl_statement : IDENTIFIER EQUALS expression
        """
        debug("Reassign", p[1])
        p[0] = AST(action='reassign', params=[p[1], p[3]])

    def p_multiple_statement(self, p):
        """
        statement_list : statement
                       | decl_statement
                       | statement_list SEMICOLON statement
                       | statement_list SEMICOLON decl_statement
        """
        if len(p) > 2:
            debug("MULTIPLE1", p[1], p[2])
            p[0] = p[1] + [p[3]]
        else:
            debug("MULTIPLE2", p[1])
            p[0] = [p[1]]

    def p_print_statement(self, p):
        """
        statement : PRINT LPAREN expr_list RPAREN
        """
        p[0] = AST(action='print', params=p[3])

    def p_expression_bool_true(self, p):
        """
        expression : TRUE
        """
        p[0] = p[1]

    def p_expression_bool_false(self, p):
        """
        expression : FALSE
        """
        p[0] = p[1]

    def p_expression_var(self, p):
        """
        expression : IDENTIFIER
        """
        p[0] = AST(action='get', params=[p[1]])

    def p_expression_float(self, p):
        """
        expression : FLOATCONST
        """
        p[0] = float(p[1])

    def p_expression_integer(self, p):
        """
        expression : INTCONST
        """
        p[0] = int(p[1])

    def p_expression_string(self, p):
        """
        expression : STRINGCONST
        """
        p[0] = str(p[1])

    def p_expression_neg(self, p):
        """
        expression : MINUS expression %prec NEGATE
        """
        p[0] = AST(action='binop', params=[-1, '*', p[1]])

    def p_expression_binop(self, p):
        """
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MUL expression
                   | expression DIV expression
                   | expression MOD expression
                   | expression POW expression
                   | expression GT expression
                   | expression GE expression
                   | expression LT expression
                   | expression LE expression
                   | expression EQ expression
                   | expression NE expression
        """
        p[0] = AST(action='binop', params=p[1:])

    def p_expression_increment(self, p):
        """
        expression : IDENTIFIER PLUSPLUS
        """
        p[0] = AST(action='binop', params=[p[1], '+', 1])

    def p_expression_decrement(self, p):
        """
        expression : IDENTIFIER MINUSMINUS
        """
        p[0] = AST(action='binop', params=[p[1], '-', 1])

    def p_expression_list(self, p):
        """
        expr_list : expression
                  | expr_list COMMA expression

        """
        if len(p) > 2:
            p[0] = p[1] + [p[3]]
        else:
            p[0] = [p[1]]

    def p_expression_parens(self, p):
        """
        expression : LPAREN expression RPAREN
        """
        p[0] = p[2]

    def p_error(self, p):
        raise SyntaxError("invalid syntax")

    def p_empty(self, p):
        """empty :"""
        pass

    def build(self):
        self.parser = yacc.yacc(module=self)
        return self.parser


def debug(*params):
    if DEBUG_MODE:
        print("[DBG] %s" % (' : '.join(str(x) for x in params),))