"""
Abstract Syntax Tree

AST class handles visiting nodes and resolving nodes containing multiple recursive
operations. All nodes are encapsulated within one class "AST" and called directly
from the "eval" method. A list of all the nodes is stored in its parameters and
evaluated based on control flow.
"""

DEBUG_MODE = True
symbols = {'global': {}, 'local': {}}  # holds symbols for variables
state = ["global"]  # a stack that holds current variable state and scope
function_state = []  # a stack that holds current scope of functions
scope_needed = ['IfElseStmt', 'IfStmt', 'ElseStmt', 'ForStmt']  # stores different states for when a scope is needed


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
        if isinstance(node.param, list):
            new_list = []
            for elem in node.param:
                new_list.append(self.visit(elem))
            return new_list

        return node.param

    def visit_List(self, node):
        debug("LIST PROCESSING", node, node.action, node.param)
        if node.action == 'get':
            # Accepts in the form of ListID[expr_list] : param = [IDENTIFIER, expr_list]
            # Get the list variable
            arr = self.visit(Variable(action='get', param=Literal(action="IDEN", param=node.param[0])))
            index = []

            for idx in node.param[1]:  # resolve each indices
                index.append(self.visit(idx))

            for idx in index:
                if not isinstance(idx, int):
                    raise TypeError(f"list indices must be integers or slices, not {type(idx)}")
                elif 0 <= idx < len(arr):
                    arr = arr[idx]
                else:
                    raise IndexError("list index out of range")

            return arr

        elif node.action == 'assign':
            # Accepts in the form of ListID[expr_list] = expr : param = [IDENTIFIER, expr_list, expr]
            arr = self.visit(Variable(action='get', param=Literal(action='IDEN', param=node.param[0])))
            index = []

            for idx in node.param[1]:
                index.append(self.visit(idx))

            assignment = self.visit(node.param[2])

            for idx in index[:-1]:
                if idx < 0 or idx > len(arr):
                    raise IndexError("list index out of range")
                else:
                    arr = arr[idx]

            arr[index[-1]] = assignment

        elif node.action == 'slice':
            # Accepts in the form of ListID[expr : expr : expr] : param = [IDENTIFIER, expr, expr, expr | 1 default]
            arr = self.visit(Variable(action='get', param=Literal(action='IDEN', param=node.param[0])))
            start = self.visit(node.param[1])
            end = self.visit(node.param[2])
            step = self.visit(node.param[3])

            if any(not isinstance(param, int) for param in [start, end, step]):
                raise TypeError("slice indices must be integers")

            return arr[start:end:step]

        elif node.action == 'range':
            # Accepts in the form of [INT...INT] or [INT...INT, expr] : param = range
            return self.visit(node.param)  # returns a list of range

    def visit_Print(self, node):
        debug("PRINT", node, node.action, node.param)

        print(' '.join(str(self.visit(x)) for x in list(node.param)))

    def visit_Variable(self, node):
        debug("VARIABLE", node, node.action, node.param, symbols)
        if len(function_state) != 0:
            local_symbols = symbols['local'][function_state[0]]
            # end scope search at local, which is on top of function scope
            global_idx = state.index(function_state[0])
        else:
            local_symbols = symbols['local']
            global_idx = -1
        if node.action == 'assign':
            # visit right hand side to see what value it holds
            lhs = node.param[0]
            rhs = self.visit(node.param[1])
            if lhs in symbols['global'] or lhs in [local_symbols[scope] for scope in state[1:global_idx]]:
                raise NameError(f"name '{node.param[0]}' already exist")
            if state[0] in local_symbols:
                # local key only exists if it is added in different scopes
                print("STATE RIGHT NOW", state[0])
                local_symbols[state[0]][lhs] = rhs
            else:
                symbols['global'][lhs] = rhs

            return rhs

        elif node.action == 'reassign' or node.action == 'reassign_get':
            error = True
            lhs = node.param[0]
            rhs = self.visit(node.param[1])
            if lhs in symbols['global']:
                symbols['global'][lhs] = rhs
                error = False

                if node.action == 'reassign_get':
                    return symbols['global'][lhs]

            elif lhs not in symbols['global']:
                if state[0] in local_symbols:
                    var_scope = ""
                    for scope in state[:global_idx]:  # search all local states except last scope: global
                        if lhs in local_symbols[scope]:
                            local_symbols[scope][lhs] = rhs
                            error = False
                            var_scope = scope

                    if node.action == 'reassign_get':
                        return local_symbols[var_scope][lhs]

            if error:
                raise NameError(f"name '{node.param[0]}' not defined")

        elif node.action == 'get':
            identifier = self.visit(node.param)
            if identifier in symbols['global']:
                return symbols['global'][identifier]
            elif identifier not in symbols['global']:
                print("ARGUMENT", state[:global_idx])
                for scope in state[:global_idx]:  # move up a scope and check if variable exists
                    if identifier in local_symbols[scope]:
                        return local_symbols[scope][identifier]

            raise NameError(f"name '{identifier}' not defined")

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

    def visit_VariableBinopReassign(self, node):
        debug("VARIABLE BINOP REASSIGN", node, node.action, node.param)
        op = {
            '+=': '+',
            '-=': '-',
            '*=': '*',
            '/=': '/',
            '%=': '%',
            '^=': '^',
        }[node.action]

        result = self.visit(BinaryOp(action='binop', param=[node.param[0], op, node.param[1]]))

        return result

    def visit_VariableIncrDecr(self, node):
        debug("INCREMENT OR DECREMENT", node, node.action, node.param)
        op = {
            '++': '+',
            '--': '-'
        }[node.action]

        result = self.visit(BinaryOp(action='binop', param=[node.param, op, Literal(action='INTCONST', param=1)]))

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
        local_symbols = self.determine_local()
        # holds evaluation of an if statement and returns if an else will be evaluated
        # node.param[0] holds the condition and node.param[1] holds the basic block
        debug("IF STATEMENT", node, node.action, node.param)
        evaluated = False
        self.add_scope('if', local_symbols)

        if self.visit(node.param[0]):
            # since operations are basic blocks, they are always in list format
            for actions in node.param[1]:
                self.visit(actions)

            evaluated = True  # for if else statements, method will decide whether else is needed

        self.reset_scope(local_symbols)

        return False if not evaluated else True

    def visit_ElseStmt(self, node):
        local_symbols = self.determine_local()
        debug("ELSE STATEMENT", node, node.action, node.param)
        self.add_scope('else', local_symbols)

        if isinstance(node.param, list):
            for actions in node.param:
                self.visit(actions)
        else:
            self.visit(node.param)

        self.reset_scope(local_symbols)

    def visit_Range(self, node):
        debug("RANGE", node, node.action, node.param)
        start = self.visit(node.param[0])
        end = self.visit(node.param[1])
        step = self.visit(node.param[2])

        error = ""
        if not isinstance(start, int):
            error = type(start)
        elif not isinstance(end, int):
            error = type(end)
        elif not isinstance(step, int):
            error = type(step)

        if error:
            raise TypeError(f"'{error}' object cannot be interpreted as an integer")

        return list(range(start, end, step))

    def visit_ForStmt(self, node):
        # Accepts param = [iterating symbol, range of iteration, block to execute]
        local_symbols = self.determine_local()
        debug("FOR STATEMENT", node, node.action, node.param)
        loop = True
        self.add_scope('for_loop', local_symbols)
        loop_range = self.visit(node.param[1])
        iter_symbol = node.param[0]

        if not loop_range:  # empty range(0, 0)
            loop = False
        else:
            local_symbols[state[0]][iter_symbol] = loop_range[0]

        block = node.param[2]

        if loop:
            for i in loop_range:
                debug("LOOP ITER", i, loop_range, symbols)
                local_symbols[state[0]][iter_symbol] = i
                for stmt in block:
                    self.visit(stmt)  # each new scope is handled by those that need a new scope

        self.reset_scope(local_symbols)

    def visit_WhileStmt(self, node):
        # Accepts param = [conditions for while, block to execute]
        local_symbols = self.determine_local()
        debug("WHILE STATEMENT", node, node.action, node.param)
        self.add_scope("while_loop", symbols['local'])

        while self.visit(node.param[0]):
            for actions in node.param[1]:
                self.visit(actions)

        self.reset_scope(local_symbols)

    def visit_FuncBlock(self, node):
        # Called from FuncCall, params = [IDENTIFIER, exec orders]
        debug("FUNCTION BLOCK EXECUTION", node, node.action, node.param)
        for actions in node.param[1]:
            self.visit(actions)

        self.reset_scope_func_decl()

    def visit_FuncCall(self, node):
        debug("FUNCTION CALL", node, node.action, node.param)
        if node.action == 'exec':
            # Accepts function execution FuncID(expr_list), param = [IDENTIFIER, expr_list]
            func_scope = self.add_func_scope(node.param[0])  # add scope and get key for FuncDecl
            func = symbols['global'][func_scope]  # get function object
            func_local = symbols['local'][func_scope]['params']
            update_params = [self.visit(param) for param in node.param[1]]

            # Check for the number of positional arguments
            if len(update_params) < len(func_local.keys()):
                raise TypeError(f"{node.param[0]}() missing {len(func_local) - len(update_params)} required "
                                f"positional argument")
            elif len(update_params) > len(func_local.keys()):
                raise TypeError(f"{node.param[0]}() takes {len(func_local.keys())} positional arguments but "
                                f"{len(update_params)} were given")

            # update the local parameters in the local function symbols
            for i, key in enumerate(func_local.keys()):
                func_local[key] = update_params[i]

            # change object within global function key and get execution orders if first time calling
            if func.__class__.__name__ == "FuncDecl":
                exec_orders = func.param[2]
                symbols['global'][func_scope] = FuncBlock(action='func_block', param=[func_scope, exec_orders])

            # execute function
            self.visit(symbols['global'][func_scope])

    def visit_FuncDecl(self, node):
        # Accepts function block, param = [IDENTIFIER, expr_list, execution block]
        debug("FUNCTION DECLARE", node, node.action, node.param)
        # func_states = list(filter(lambda a: a.startswith('func'), symbols['local'].keys()))
        func_scope = self.add_func_scope(node.param[0])
        print(state, function_state)
        symbols['local'][func_scope] = {'params': {}}
        print(node.param[1][0].param)

        for var_param in node.param[1]:
            self.visit(var_param)

        symbols['global'][func_scope] = node
        print("UPDATED SYMBOLS", symbols, symbols['global'][func_scope].param)

        self.reset_scope_func_decl()

    def add_scope(self, scope, location):
        scope_number = 0  # the higher the number, the deeper the scope
        new_state = scope + str(scope_number)

        # search for existing scopes and rename until a new name is found
        while new_state in state:
            scope_number += 1
            new_state = scope + str(scope_number)
        state.insert(0, new_state)  # create push a new scope to the stack
        location[new_state] = {}  # create a new scope to store local variables

        return new_state

    def add_func_scope(self, scope):
        new_state = 'func_' + scope
        state.insert(0, new_state)
        state.insert(0, 'params')
        function_state.insert(0, new_state)

        return new_state

    def determine_local(self):
        if len(function_state) != 0:
            return symbols['local'][function_state[0]]
        else:
            return symbols['local']

    def reset_scope_func_decl(self):
        state.pop(0)
        state.pop(0)
        function_state.pop(0)

    def reset_scope(self, location):
        location.pop(state[0])
        state.pop(0)


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


class VariableBinopReassign(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class VariableIncrDecr(Node):
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


class Range(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class ForStmt(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class WhileStmt(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class List(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class FuncDecl(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class FuncCall(Node):
    def __init__(self, action, param):
        super().__init__(action, param)


class FuncBlock(Node):
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
