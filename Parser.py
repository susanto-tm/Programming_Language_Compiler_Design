import ply.yacc as yacc
from Lexer import Lexer
from AST import *

astList = []
DEBUG_MODE = True


class Parser:
    tokens = Lexer.tokens
    precedence = (
        ('left', 'COND'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('right', 'POW')
    )

    def p_program(self, p):
        """
        program : commands
        """
        #print(astList)
        p[0] = AST(action='eval', param=astList)

    def p_commands(self, p):
        """
        commands : commands basic_block
                 | empty
        """
        if len(p) > 2:
            debug("Adding command", )
            astList.extend(p[2])
            p[0] = p[2]
        else:
            debug("COMMANDS", p[1:])

    def p_basic_block(self, p):
        """
        basic_block : line_statement
                    | basic_block line_statement
        """
        if len(p) > 2:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_line_statement(self, p):
        """
        line_statement : statement SEMICOLON
        """
        debug("Statement", p[1].__class__.__name__, p[1].action, p[1].param)
        p[0] = p[1]

    def p_if_else_statement(self, p):
        """
        line_statement : if_line
                       | if_line else_line
        """
        if len(p) > 2:
            debug("IF ELSE BLOCK", p[1].__class__.__name__, p[2].__class__.__name__)
            p[0] = IfElseBlock(action='if-else', param=[p[1], p[2]])
        else:
            debug("IF ELSE LINE STMT", p[1].__class__.__name__, p[1].action, p[1].param)
            p[0] = p[1]

    def p_for_loop_statement(self, p):
        """
        line_statement : for_line
        """
        p[0] = p[1]

    def p_print_statement(self, p):
        """
        statement : PRINT LPAREN expr_list RPAREN
        """
        debug("PRINT", p[3])
        p[0] = Print(action='print', param=p[3])

    def p_assign(self, p):
        """
        statement : LET IDENTIFIER EQUALS expr
        """
        debug("Assignment", p[4].action)
        p[0] = Variable(action='assign', param=[p[2], p[4]])

    def p_reassign(self, p):
        """
        statement : IDENTIFIER EQUALS expr
        """
        p[0] = Variable(action='reassign', param=[p[1], p[3]])

    def p_expr_list(self, p):
        """
        expr_list : expr
                  | cond_list
                  | expr_list expr
        """
        if len(p) > 2:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = p[1]

    def p_binop(self, p):
        """
        expr : expr PLUS expr
             | expr MINUS expr
             | expr MUL expr
             | expr DIV expr
             | expr MOD expr
             | expr POW expr
             | expr LE expr
             | expr GE expr
             | expr LT expr
             | expr GT expr
             | expr EQ expr
             | expr NE expr
        """
        p[0] = BinaryOp(action='binop', param=p[1:])

    def p_increment(self, p):
        """
        expr : expr PLUSPLUS
        """
        p[0] = BinaryOp(action='binop', param=[p[1], '+', Literal(action='INTCONST', param=1)])

    def p_decrement(self, p):
        """
        expr : expr MINUSMINUS
        """
        p[0] = BinaryOp(action='binop', param=[p[1], '-', Literal(action='INTCONST', param=1)])

    def p_iden(self, p):
        """
        expr : IDENTIFIER
        """
        p[0] = Variable(action='get', param=Literal(action='IDEN', param=p[1]))

    def p_integer_const(self, p):
        """
        expr : INTCONST
        """
        p[0] = Literal(action='INTCONST', param=int(p[1]))

    def p_float_const(self, p):
        """
        expr : FLOATCONST
        """
        p[0] = Literal(action="FLOATCONST", param=float(p[1]))

    def p_string_const(self, p):
        """
        expr : STRINGCONST
        """
        p[0] = Literal(action="STRINGCONST", param=str(p[1]))

    def p_boolean(self, p):
        """
        expr : TRUE
             | FALSE
        """
        expr = None
        if p[1] == 'true':
            expr = True
        elif p[1] == 'false':
            expr = False

        p[0] = Literal(action='BOOLEAN', param=bool(expr))

    def p_expr_paren(self, p):
        """
        expr : LPAREN expr RPAREN
        """
        p[0] = p[2]

    def p_cond_list(self, p):
        """
        cond_list : expr %prec COND
                  | cond_list AND expr
                  | cond_list OR expr
        """
        if len(p) > 2:
            p[0] = BoolOp(action='boolop', param=p[1:])
        else:
            p[0] = p[1]

    def p_if_stmt(self, p):
        """
        if_line : IF cond_list LBRACE basic_block RBRACE
        """
        debug("IF DECL", p[2], p[4])
        p[0] = IfStmt(action='if_branch', param=[p[2], p[4]])

    def p_else_line(self, p):
        """
        else_line : ELSE LBRACE basic_block RBRACE
        """
        debug("ELSE DECL", p[3])
        p[0] = ElseStmt(action='else_branch', param=p[3])

    def p_for_line(self, p):
        """
        for_line : FOR IDENTIFIER WALRUS range LBRACE basic_block RBRACE
        """
        p[0] = ForStmt(action='for_loop', param=[p[2], p[4], p[6]])

    def p_range_generator(self, p):
        """
        range : LPAREN expr ELLIPSIS expr RPAREN
        """
        p[0] = Range(action='range_decl', param=[p[2], p[4]])

    def p_empty(self, p):
        """
        empty :
        """
        pass

    def build(self):
        self.parser = yacc.yacc(module=self)
        return self.parser


def debug(*params):
    if DEBUG_MODE:
        print("[DBG] %s" % (' : '.join(str(x) for x in params),))