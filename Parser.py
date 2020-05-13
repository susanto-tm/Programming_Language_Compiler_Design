import lex_yacc.yacc as yacc
from Lexer import Lexer
from AST import *

astList = []
DEBUG_MODE = False


class Parser:
    tokens = Lexer.tokens
    precedence = (
        ('left', 'COND'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('right', 'POW'),
        ('right', 'NEGATE')
    )

    def p_program(self, p):
        """
        program : commands
        """
        # print(astList)
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
                       | while_line
                       | func_line
                       | switch_line
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
                  | LET IDENTIFIER
        """
        if len(p) > 3:
            debug("Assignment", p[4].action)
            p[0] = Variable(action='assign', param=[p[2], p[4]])
        else:
            debug("Assignment", p[2])
            p[0] = Variable(action='assign', param=[p[2], Literal(action='INTCONST', param=0)])

    def p_reassign(self, p):
        """
        statement : IDENTIFIER EQUALS expr
        """
        p[0] = Variable(action='reassign', param=[p[1], p[3]])

    def p_reassign_plus_equals(self, p):
        """
        statement : IDENTIFIER PLUSEQUALS expr
                  | IDENTIFIER MINUSEQUALS expr
                  | IDENTIFIER MULEQUALS expr
                  | IDENTIFIER DIVEQUALS expr
                  | IDENTIFIER MODEQUALS expr
                  | IDENTIFIER POWEQUALS expr
        """
        p[0] = Variable(action='reassign', param=[p[1], VariableBinopReassign(action=p[2], param=[
            Variable(action='get', param=Literal(action='IDEN', param=p[1])), p[3]])])

    def p_incr_decr_statement(self, p):
        """
        statement : incr_decr
        """
        p[0] = p[1]

    def p_list_assign_statement(self, p):
        """
        statement : IDENTIFIER LBRACKET expr_list RBRACKET EQUALS expr
        """
        p[0] = List(action='assign', param=[p[1], p[3], p[6]])

    def p_func_call_statement(self, p):
        """
        statement : func_call
        """
        p[0] = p[1]

    def p_func_math_statement(self, p):
        """
        statement : IDENTIFIER LPAREN expr_list RPAREN EQUALS expr
        """
        p[0] = FuncDecl(action='func_math', param=[p[1], p[3], [p[6]]])

    def p_return_statement(self, p):
        """
        statement : RETURN expr_list
        """
        p[0] = ReturnStmt(action='return_stmt', param=p[2])

    def p_break_statement(self, p):
        """
        statement : BREAK
        """
        p[0] = BreakStmt(action='break', param=p[1])

    def p_expr_list(self, p):
        """
        expr_list : expr
                  | cond_list
                  | expr_list COMMA expr
                  | empty
        """
        if len(p) > 2:
            p[0] = p[1] + [p[3]]
        elif p[1] is not None:
            p[0] = [p[1]]
        else:
            p[0] = p[1]

    def p_assign_expr(self, p):
        """
        expr : LET IDENTIFIER
        """
        p[0] = Variable(action='assign', param=[p[2], Literal(action='INTCONST', param=0)])

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

    def p_unary_negate(self, p):
        """
        expr : MINUS expr %prec NEGATE
        """
        p[0] = BinaryOp(action='binop', param=[
            Literal(action='INTCONST', param=-1),
            '*',
            p[2]
        ])

    def p_increment_decrement(self, p):
        """
        incr_decr : IDENTIFIER PLUSPLUS
                  | IDENTIFIER MINUSMINUS
        """
        p[0] = Variable(action='reassign_get', param=[
            p[1],
            VariableIncrDecr(action=p[2], param=Variable(action='get', param=Literal(action="IDEN", param=p[1])))])

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

    def p_list_const(self, p):
        """
        expr : LBRACKET expr_list RBRACKET
        """
        p[0] = Literal(action="LISTCONST", param=list(p[2]))

    def p_list_const_generate(self, p):
        """
        expr : LBRACKET range RBRACKET
        """
        p[0] = List(action='range', param=p[2])

    def p_list_indexing(self, p):
        """
        expr : IDENTIFIER LBRACKET expr_list RBRACKET
        """
        p[0] = List(action='get', param=[p[1], p[3]])

    def p_list_slicing(self, p):
        """
        expr : IDENTIFIER LBRACKET expr COLON expr RBRACKET
             | IDENTIFIER LBRACKET expr COLON expr COLON expr RBRACKET
        """
        if len(p) > 7:
            p[0] = List(action='slice', param=[p[1], p[3], p[5], p[7]])
        else:
            p[0] = List(action='slice', param=[p[1], p[3], p[5],
                                               Literal(action='INTCONST', param=1)])

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

    def p_null(self, p):
        """
        expr : NULL
        """
        p[0] = Literal(action='NULL', param=None)

    def p_expr_paren(self, p):
        """
        expr : LPAREN expr RPAREN
        """
        p[0] = p[2]

    def p_expr_incr_decr(self, p):
        """
        expr : incr_decr
        """
        p[0] = p[1]

    def p_func_call_expr(self, p):
        """
        expr : func_call
        """
        p[0] = p[1]

    def p_func_call_len(self, p):
        """
        expr : LEN LPAREN expr RPAREN
        """
        p[0] = FuncCall(action='len', param=p[3])

    def p_func_call_trig(self, p):
        """
        expr : SIN LPAREN expr_list RPAREN
             | COS LPAREN expr_list RPAREN
             | TAN LPAREN expr_list RPAREN
             | ASIN LPAREN expr_list RPAREN
             | ACOS LPAREN expr_list RPAREN
             | ATAN LPAREN expr_list RPAREN
             | SINH LPAREN expr_list RPAREN
             | COSH LPAREN expr_list RPAREN
             | TANH LPAREN expr_list RPAREN
        """
        debug("TRIG FUNCTION", p[1], p[3])
        p[0] = FuncCall(action='trig', param=[p[1], p[3]])

    def p_func_call_integrate(self, p):
        """
        expr : INTEGRATE LPAREN expr_list RPAREN
        """
        debug("INTEGRATION", p[1], p[3])
        p[0] = FuncCall(action='integral', param=[p[1], p[3]])

    def p_func_call_derivative(self, p):
        """
        expr : DIFF LPAREN expr_list RPAREN
        """
        debug("DIFFERENTIATION", p[1], p[3])
        p[0] = FuncCall(action='deriv', param=[p[1], p[3]])

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
        for_line : FOR IDENTIFIER WALRUS RANGE range LBRACE basic_block RBRACE
        """
        p[0] = ForStmt(action='for_loop', param=[p[2], p[5], p[7]])

    def p_for_line_single_range(self, p):
        """
        for_line : FOR IDENTIFIER WALRUS RANGE expr LBRACE basic_block RBRACE
        """
        p[0] = ForStmt(action='for_loop', param=[
            p[2],
            Range(action='range_decl', param=[Literal(action='INTCONST', param=0),
                                              p[5],
                                              Literal(action='INTCONST', param=1)]),p[7]])

    def p_while_line(self, p):
        """
        while_line : FOR cond_list LBRACE basic_block RBRACE
        """
        p[0] = WhileStmt(action='while_loop', param=[p[2], p[4]])

    def p_range_generator(self, p):
        """
        range : expr ELLIPSIS expr
              | expr ELLIPSIS expr COMMA expr
        """
        if len(p) > 4:
            p[0] = Range(action='range_decl', param=[p[1], p[3], p[5]])
        else:
            p[0] = Range(action='range_decl', param=[p[1], p[3], Literal(action='INTCONST', param=1)])

    def p_function_line(self, p):
        """
        func_line : FUNC IDENTIFIER LPAREN expr_list RPAREN LBRACE basic_block RBRACE
        """
        p[0] = FuncDecl(action='func_block', param=[p[2], p[4], p[7]])

    def p_function_call(self, p):
        """
        func_call : IDENTIFIER LPAREN expr_list RPAREN
        """
        p[0] = FuncCall(action='exec', param=[p[1], p[3]])

    def p_switch_line(self, p):
        """
        switch_line : SWITCH LPAREN expr RPAREN LBRACE case_list RBRACE
        """
        p[0] = SwitchStmt(action='switch', param=[p[3], p[6]])

    def p_case_list(self, p):
        """
        case_list : case_block
                  | case_list case_block
        """
        if len(p) > 2:
            p[0] = p[1] + [p[2]]
        else:
            p[0] = [p[1]]

    def p_switch_case(self, p):
        """
        case_block : CASE expr LBRACE basic_block RBRACE
        """
        debug("CASE BLOCK", p[1], p[2], p[4])
        p[0] = CaseStmt(action='case', param=[p[2], p[4]])

    def p_default_case(self, p):
        """
        case_block : DEFAULT LBRACE basic_block RBRACE
        """
        debug("DEFAULT CASE", p[1], p[3])
        p[0] = DefaultStmt(action='default', param=p[3])

    def p_empty(self, p):
        """
        empty :
        """
        pass

    def p_error(self, p):
        raise SyntaxError("invalid syntax")

    def build(self):
        self.parser = yacc.yacc(module=self)
        return self.parser


def debug(*params):
    if DEBUG_MODE:
        print("[DBG] %s" % (' : '.join(str(x) for x in params),))
