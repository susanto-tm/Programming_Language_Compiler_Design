import lex_yacc.lex as lex

DEBUG_MODE = False


class Lexer:
    states = (
        ('string', 'inclusive'),
    )
    reserved = (
        'AND', 'ATAN', 'ACOS', 'ASIN', 'BREAK', 'CASE', 'COS', 'COSH', 'DEFAULT', 'DIFF', 'ELSE', 'FOR',
        'FALSE', 'FLOAT', 'FUNC', 'INT', 'IF', 'INTEGRATE', 'LET', 'LIST', 'LEN', 'MIN', 'MAX', 'NOT', 'NULL',
        'OR', 'PRINT', 'RETURN', 'RANGE', 'SWITCH', 'STR', 'SIN', 'SINH', 'TRUE', 'TYPE', 'TAN', 'TANH',
    )

    tokens = reserved + (
        # Literals (identifiers, integer identifier, float identifier, string identifier)
        'IDENTIFIER', 'INTCONST', 'FLOATCONST', 'STRINGCONST',

        # Function Properties

        # Operators (+, -, *, /, %, ^, <=, >=, <, >, ==, !=)
        'PLUS', "MINUS", 'MUL', 'DIV', 'MOD', 'POW',
        'LE', 'GE', 'LT', 'GT',
        'EQ', 'NE',

        # Assignment (=, *=, /=, +=, -=, %=, ^=, :=)
        'EQUALS', 'MULEQUALS', 'DIVEQUALS', 'PLUSEQUALS', 'MINUSEQUALS', 'MODEQUALS', 'POWEQUALS', 'WALRUS',

        # Increment/Decrement (++, --)
        'PLUSPLUS', 'MINUSMINUS',

        # Delimiters ( ) [ ] { } , . ; :
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON', 'COLON',

        # Ellipsis (...)
        'ELLIPSIS',
    )

    reserved_map = {r.lower(): r for r in reserved}

    # Ignore spaces and tabs
    t_ignore = ' \t\n'

    # Operators
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_MOD = r'\%'
    t_POW = r'\^'
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_GT = r'>'
    t_EQ = r'=='
    t_NE = r'!='

    # Increment / Decrement
    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'\-\-'

    # Booleans

    # Assignment
    t_EQUALS = r'='
    t_MULEQUALS = r'\*='
    t_DIVEQUALS = r'/='
    t_PLUSEQUALS = r'\+='
    t_MINUSEQUALS = r'\-='
    t_MODEQUALS = r'\%='
    t_POWEQUALS = r'\^='
    t_WALRUS = r'\:='

    # Delimiters
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA = r'\,'
    t_SEMICOLON = r'\;'
    t_COLON = r'\:'

    # Ellipsis
    t_ELLIPSIS = r'\.\.\.'

    # Token definitions with action code
    def t_COMMENT(self, t):
        r'\/\/.*'
        pass

    def t_IDENTIFIER(self, t):
        r'[A-Za-z][A-Za-z0-9_]*'
        t.type = self.reserved_map.get(t.value, 'IDENTIFIER')
        return t

    # Precedence of floats takes over integers
    def t_FLOATCONST(self, t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INTCONST(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRINGCONST(self, t):
        r'[\"|\']'
        t.lexer.begin('string')
        t.lexer.str_start = t.lexer.lexpos
        t.lexer.str_marker = t.value

    def t_string_chars(self, t):
        r'[^\"\'\n]+'

    def t_string_end(self, t):
        r'[\"\']'

        if t.lexer.str_marker == t.value:
            t.type = 'STRINGCONST'
            t.value = t.lexer.lexdata[t.lexer.str_start:t.lexer.lexpos - 1]
            t.lexer.begin('INITIAL')
            return t

    def t_error(self, t):
        print("Illegal Character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        global SHOW_LEX, DEBUG_MODE
        self.lexer = lex.lex(module=self, **kwargs)

    # Pass input and test lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)

