import ply.yacc as yacc
from Lexer import Lexer
from Other_Designs.Compiler2 import AST
from Other_Designs import Compiler2

DEBUG_MODE = True
astPrec = []


class Parser:
    tokens = Lexer.tokens
    precedence = (
        # ('nonassoc', 'LOOP_INSTRUCT'),
        ('nonassoc', 'IFX'),
        ('left', 'CONDITION'),
        ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('right', 'POW'),
        ('right', 'NEGATE')
    )

    def p_program(self, p):
        """
        program : commands
        """
        p[0] = astPrec

    def p_commands(self, p):
        """
        commands : commands statement SEMICOLON
                 | commands line_statement
                 | commands conditional_block
                 | empty
        """
        if len(p) > 2:
            debug("COMMANDS", str(p[2]))
            if isinstance(p[2], list):
                astPrec.extend(p[2])
            else:
                astPrec.append(p[2])
            debug("ASTPREC", [x.action for x in astPrec])
            p[0] = p[2]
        else:
            debug("COMMANDS", p[1:])


    def p_line_statement(self, p):
        """
        line_statement : line_statement statement SEMICOLON
                       | line_statement expression SEMICOLON
                       | empty
        """
        if len(p) > 2:
            debug("LINE STMT", type(p[1]))
            p[0] = [p[1]]
            p[0].append(p[2])

    def p_declaration(self, p):
        """
        line_statement : LET IDENTIFIER EQUALS expression SEMICOLON
                       | LET IDENTIFIER SEMICOLON
        """
        if len(p) > 4:
            debug("ID ASSIGN-E", p[2], p[4])
            p[0] = AST(action='assign', params=[p[2], p[4]])
            debug("SYMBOLS", Compiler2.symbols)
        else:
            debug("ID ASSIGN 0", p[2])
            p[0] = AST(action='assign', params=[p[2], 0])

    def p_declaration_reassign(self, p):
        """
        line_statement : IDENTIFIER EQUALS expression SEMICOLON
        """
        debug("REASSIGN", p[1])
        p[0] = AST(action='reassign', params=[p[1], p[3]])

    def p_print_statement(self, p):
        """
        statement : PRINT LPAREN expr_list RPAREN
        """
        debug("PRINT", p[3])
        p[0] = AST(action='print', params=p[3])

    def p_expression_list(self, p):
        """
        expr_list : expression
                  | expr_list COMMA expression
        """
        if len(p) > 2:
            p[0] = p[1] + [p[3]]
        else:
            debug("EXPRL", [p[1]])
            p[0] = [p[1]]

    def p_expression_bool_true(self, p):
        """
        expression : TRUE
        """
        p[0] = True

    def p_expression_bool_false(self, p):
        """
        expression : FALSE
        """
        debug("FALSE", type(p[1]))
        p[0] = False

    def p_expression_var(self, p):
        """
        expression : IDENTIFIER
        """
        debug("EXPR IDEN", p[1])
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
        p[0] = AST(action='binop', params=[-1, '*', p[2]])

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
        debug("BINOP", p[1], p[3])
        p[0] = AST(action='binop', params=p[1:])

    def p_expression_increment(self, p):
        """
        expression : IDENTIFIER PLUSPLUS
        """
        debug("PLUSPLUS", p[1])
        p[0] = AST(action='binop', params=[AST(action='get', params=[p[1]]), '+', 1])

    def p_expression_decrement(self, p):
        """
        expression : IDENTIFIER MINUSMINUS
        """
        debug("MINUSMINUS", p[1])
        p[0] = AST(action='binop', params=[AST(action='get', params=[p[1]]), '-', 1])


    def p_expression_parens(self, p):
        """
        expression : LPAREN expression RPAREN
        """
        p[0] = p[2]

    def p_statement_condition(self, p):
        """
        conditional_block : IF condition_list LBRACE line_statement RBRACE %prec IFX
        """
        if len(p) > 5:
            debug("IF", p[2], [str(x) for x in p[1:]])
            p[0] = AST(action='condition', params=[p[2], p[4]])
        else:
            if p[1][1] != "if":
                raise SyntaxError
            else:
                p[0] = AST(action='condition', params=[p[1][3], p[1][6], p[4]])

    def p_condition_list(self, p):
        """
        condition_list : expression %prec CONDITION
                       | condition_list AND expression
                       | condition_list OR expression
        """
        if len(p) > 2:
            p[0] = AST(action='boolop', params=p[1:])
        else:
            debug("CONDITION", p[1].compile(), p[1])
            p[0] = p[1]

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