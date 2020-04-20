from rply import LexerGenerator, Token

lg = LexerGenerator()

reserved = (
    'and', 'break', 'case', 'continue', 'default', 'else', 'for', 'float', 'from', 'if', 'int', 'integrate', 'let',
    'not', 'or', 'print', 'return', 'switch', 'string', 'to', 'type', 'while',
)


# Literals
lg.add("IDENTIFIER", r'[A-Za-z][A-Za-z0-9]*')
lg.add("FLOATCONST", r'\d+\.\d+')
lg.add("INTCONST", r'\d+')
lg.add("STRINGCONST", r'\'.*\'|\".*\"')

# Operators
lg.add("PLUS", r'\+')
lg.add("MINUS", r'\-')
lg.add("MUL", r'\*')
lg.add("DIV", r'/')
lg.add("POW", r'\^')
lg.add("LE", r'<=')
lg.add("GE", r'>=')
lg.add("LT", r'<')
lg.add("GT", r'>')
lg.add("EQ", r'==')
lg.add("NE", r'!=')

# Assignment
lg.add("EQUALS", r'=')
lg.add("MULEQUALS", r'\*=')
lg.add("DIVEQUALS", r'/=')
lg.add("PLUSEQUALS", r'\+=')
lg.add("MINUSEQUALS", r'-=')

# Increment / Decrement
lg.add("PLUSPLUS", r'\+\+')
lg.add("MINUSMINUS", r'--')

# Delimiters
lg.add("LPAREN", r'\(')
lg.add("RPAREN", r'\)')
lg.add("LBRACKET", r'\[')
lg.add("RBRACKET", r'\]')
lg.add("LBRACE", r'\{')
lg.add("RBRACE", r'\}')
lg.add("COMMA", r'\,')
lg.add("PERIOD", r'\.')
lg.add("SEMICOLON", r'\;')
lg.add("COLON", r'\:')

# Ellipsis
lg.add("ELLIPSIS", r'\.\.\.')

# Ignore spaces and tabs
lg.ignore('\s+')

lexer = lg.build()


def reserved_identifier(token):
    if token.value.lower() in reserved:
        return Token(token.value.upper(), token.value)
    return token


callbacks = {"IDENTIFIER": [reserved_identifier]}
token_names = [rule.name for rule in lg.rules] + [name.upper() for name in reserved]


def lex(buf):
    for token in lexer.lex(buf):
        for callback in callbacks.get(token.name, []):
            token = callback(token)
        yield token


if __name__ == "__main__":
    expr = input("Enter an expression: ")
    print(list(lex(expr)))
