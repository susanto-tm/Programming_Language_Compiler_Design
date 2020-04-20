import ply.lex as lex


class Lexer:
    reserved = (
        'AND', 'BREAK', 'CASE', 'CONTINUE', 'DEFAULT', 'ELSE', 'FOR', 'FLOAT', 'FROM', 'IF', 'INT', 'INTEGRATE', 'LET',
        'NOT', 'OR', 'PRINT', 'RETURN', 'SWITCH', 'STRING', 'TO', 'TYPE', 'WHILE',
    )

    tokens = reserved + (
        # Literals (identifiers, integer identifier, float identifier, string identifier)
        'IDENTIFIER', 'INTCONST', 'FLOATCONST', 'STRINGCONST',

        # Function Properties

        # Operators (+, -, *, /, ^, <=, >=, <, >, ==, !=)
        'PLUS', "MINUS", 'MUL', 'DIV', 'POW',
        'LE', 'GE', 'LT', 'GT',
        'EQ', 'NE',

        # Assignment (=, *=, /=, +=, -=)
        'EQUALS', 'MULEQUALS', 'DIVEQUALS', 'PLUSEQUALS', 'MINUSEQUALS',

        # Increment/Decrement (++, --)
        'PLUSPLUS', 'MINUSMINUS',

        # Delimiters ( ) [ ] { } , . ; :
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COMMA', 'PERIOD', 'SEMICOLON', 'COLON',

        # Ellipsis (...)
        'ELLIPSIS',
    )

    reserved_map = {r.lower(): r for r in reserved}

    # Ignore spaces and tabs
    t_ignore = ' \t'

    # Operators
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_POW = r'\^'
    t_LE = r'<='
    t_GE = r'>='
    t_LT = r'<'
    t_GT = r'>'
    t_EQ = r'=='
    t_NE = r'!='

    # Function Properties

    # Assignment
    t_EQUALS = r'='
    t_MULEQUALS = r'\*='
    t_DIVEQUALS = r'/='
    t_PLUSEQUALS = r'\+='
    t_MINUSEQUALS = r'-='

    # Increment / Decrement
    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'--'

    # Delimiters
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA = r'\,'
    t_PERIOD = r'\.'
    t_SEMICOLON = r'\;'
    t_COLON = r'\:'

    # Ellipsis
    t_ELLIPSIS = r'\.\.\.'

    # Token definitions with action code
    def t_IDENTIFIER(self, t):
        r'[A-Za-z][A-Za-z0-9_]*'
        t.type = self.reserved_map.get(t.value, 'IDENTIFIER')
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

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
        r'\'.*\'|\".*\"'
        t.value = str(t.value)
        return t

    def t_error(self, t):
        print("Illegal Character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Pass input and test lexer
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


m = Lexer()
m.build()
m.test("f(x) : int {2.0;}")







