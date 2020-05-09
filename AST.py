"""
Abstract Syntax Tree

AST class handles visiting nodes and resolving nodes containing multiple recursive
operations. All nodes are encapsulated within one class "AST" and called directly
from the "eval" method. A list of all the nodes is stored in its parameters and
evaluated based on control flow.
"""

DEBUG_MODE = True
symbols = {}  # holds symbols for variables
state = [""]  # holds current variable state and scope


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
            if 'local_' + state[0] in symbols:
                # local key only exists if it is added in different scopes
                symbols['local_'+state[0]][lhs] = rhs
            else:
                symbols[lhs] = rhs

        elif node.action == 'reassign':
            error = False
            lhs = node.param[0]
            rhs = self.visit(node.param[1])
            if 'local_'+state[0] in symbols:  # in local scope
                if lhs not in symbols:
                    if lhs not in symbols['local_'+state[0]]:
                        error = True
                    else:
                        symbols['local_'+state[0]][lhs] = rhs
                elif lhs in symbols:
                    symbols[lhs] = rhs
            elif 'local_'+state[0] not in symbols:
                if lhs in symbols:
                    symbols[lhs] = rhs
                else:
                    error = True

            if error:
                raise NameError(f"name '{node.param[0]}' not defined")

        elif node.action == 'get':
            error, local = False, 'local_'+state[0] in symbols
            identifier = self.visit(node.param)
            if symbols or local:
                if identifier in symbols:
                    return symbols[identifier]
                elif local:
                    if identifier in symbols['local_'+state[0]]:
                        return symbols['local_'+state[0]][identifier]
                    else:
                        error = True
                else:
                    error = True

            if error:
                raise (NameError(f"name '{identifier}' not defined"))

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

    def visit_IfElseBlock(self, node):
        # combines both if and else blocks to manage the control flow
        if not self.visit(node.param[0]):
            self.visit(node.param[1])

    def visit_IfStmt(self, node):
        # holds individual if statement and else statement evaluation
        # node.param[0] holds the condition and node.param[1] holds the basic block
        debug("IF STATEMENT", node, node.action, node.param)
        if self.visit(node.param[0]):
            state[0] = 'if'
            symbols['local_' + state[0]] = {}  # initialize storage of local variables
            # since parameters are basic blocks, they are always in list format
            for actions in node.param[1]:
                self.visit(actions)

            # destroy local variables
            symbols.pop('local_'+state[0])

            # reset state
            state[0] = ""

            return True  # for if else statements method will decide whether else is needed

        return False

    def visit_ElseStmt(self, node):
        debug("ELSE STATEMENT", node, node.action, node.param)
        state[0] = 'else'
        symbols['local_'+state[0]] = {}

        if isinstance(node.param, list):
            for actions in node.param:
                self.visit(actions)
        else:
            self.visit(node.param)

        # destroy local variable
        symbols.pop('local_'+state[0])

        # reset state
        state[0] = ""


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


class IfElseBlock(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class IfStmt(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class ElseStmt(Node):
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
