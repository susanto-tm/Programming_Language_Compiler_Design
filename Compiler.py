DEBUG_MODE = True
symbols = {}


def debug(*params):
    if DEBUG_MODE:
        print("[DBG] %s" % (' : '.join(str(x) for x in params),))


class AST:
    def __init__(self, action=None, params=None):
        self.action = action
        self.params = params

    def compile(self):
        result = None
        if self.action == 'print':
            print(' '.join(str(AST.resolve(x)) for x in list(self.params)))

        elif self.action == 'get':
            result = symbols.get(self.params[0], 0)

        elif self.action == 'assign':
            result = symbols[self.params[0]] = AST.resolve(self.params[1])

        elif self.action == 'reassign':
            if symbols.get(self.params[0]):
                result = symbols[self.params[0]] = AST.resolve(self.params[1])
            else:
                raise NameError("name '%s' is not defined" % self.params[0])

        elif self.action == 'condition':
            if AST.resolve(self.params[0]):
                result = AST.resolve(self.params[1])
                print(result)
            elif len(self.params) > 2:
                result = AST.resolve(self.params[2])

        elif self.action == 'boolop':
            params = list(self.params)
            result = AST.resolve(params.pop())
            while len(params) >= 2:
                prev = result
                op = AST.resolve(params.pop()).upper()
                comp = AST.resolve(params.pop())
                result = {
                    'AND': lambda a, b: a and b,
                    'OR': lambda a, b: a or b,
                }[op](prev, comp)

        elif self.action == 'binop':
            left = AST.resolve(self.params[0])
            right = AST.resolve(self.params[2])
            op = self.params[1]
            result = {
                '+': lambda l, r: l + r,
                '-': lambda l, r: l - r,
                '*': lambda l, r: l * r,
                '/': lambda l, r: l / r,
                '%': lambda l, r: l % r,
                '^': lambda l, r: l ** r,
                '>': lambda l, r: l > r,
                '>=': lambda l, r: l >= r,
                '<': lambda l, r: l < r,
                '<=': lambda l, r: l <= r,
                '==': lambda l, r: l == r,
                '!=': lambda l, r: l != r,
            }[op](left, right)

        return result

    @staticmethod
    def is_nested(x=None):
        return x is not None and isinstance(x, AST)

    @staticmethod
    def resolve(x):
        if not AST.is_nested(x):
            return x
        else:
            return x.compile()
