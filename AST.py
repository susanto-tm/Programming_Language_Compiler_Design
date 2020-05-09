"""
Abstract Syntax Tree

AST class handles visiting nodes and resolving nodes containing multiple recursive
operations. All nodes are encapsulated within one class "AST" and called directly
from the "eval" method. A list of all the nodes is stored in its parameters and
evaluated based on control flow.
"""

DEBUG_MODE = True
symbols = {}  # holds symbols for variables


class Node:
    def __init__(self, action, param):
        self.action = action
        self.param = param

    def __repr__(self):
        return f'{self.__class__.__name__}'

    __str__ = __repr__


class AST:
    def __init__(self, action, param):
        self.action = action
        self.param = param

    def eval(self):
        if self.action == 'eval':
            debug("BEGIN EXECUTION", "Params:", self.param)
            for node in self.param:
                self.visit(node)

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)

    def visit_Literal(self, node):
        return node.param

    def visit_Print(self, node):
        debug("PRINT", node, node.action, node.param)
        if isinstance(node.param, Node):
            node.param = self.visit(node.param)

        print(' '.join(str(x) for x in list([node.param])))

    def visit_Variable(self, node):
        debug("VARIABLE", node, node.action, node.param, symbols)
        if node.action == 'assign':
            # visit right hand side to see what value it holds
            lhs = node.param[0]
            rhs = self.visit(node.param[1])
            if lhs in symbols:
                raise NameError(f"name '{node.param[0]}' already exist")
            symbols[lhs] = rhs

        elif node.action == 'reassign':
            lhs = node.param[0]
            rhs = self.visit(node.param[1])
            if lhs not in symbols:
                raise NameError(f"name '{node.param[0]}' not defined")
            symbols[lhs] = rhs

        elif node.action == 'get':
            identifier = self.visit(node.param)
            if identifier not in symbols:
                raise NameError(f"name '{identifier}' not defined")
            return symbols[identifier]

    def visit_BinaryOp(self, node):
        debug("BINARY OP", node, node.action, node.param)
        left = self.visit(node.param[0])
        op = node.param[1]
        right = self.visit(node.param[2])

        result = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '%': lambda a, b: a % b,
            '^': lambda a, b: a ** b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
            '<': lambda a, b: a < b,
            '>': lambda a, b: a > b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
        }[op](left, right)

        return result

    def visit_BoolOp(self, node):
        debug("BOOLOP", node, node.action, node.param)
        params = list(node.param)
        result = self.visit(params.pop(0))
        while len(params) >= 2:
            left = result
            op = params.pop(0).upper()
            right = self.visit(params.pop(0))
            result = {
                "AND": lambda a, b: a and b,
                "OR": lambda a, b: a or b
            }[op](left, right)

        return result


"""
-----------------------------------------------------------------------------------
Node Object Definitions

# Organizes AST calls into objects to be visited and evaluated based on Class Name
-----------------------------------------------------------------------------------
"""


class Print(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class Variable(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class Literal(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class BinaryOp(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class BoolOp(Node):
    def __init__(self, action, param):
        super().__init__(action, param)

"""
-----------------------------------------------------------------------------------
Debugging Tool
-----------------------------------------------------------------------------------
"""


def debug(*params):
    if DEBUG_MODE:
        print("[DBG] %s" % (' : '.join(str(x) for x in params),))
