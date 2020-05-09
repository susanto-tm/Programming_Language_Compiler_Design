import ast


class AST:
    _action = None
    _args = []

    def __init__(self, *args, **kwargs):
        for value in args:
            self._args.append(value)

    def eval(self):
        return self._action


class Program(AST):
    def eval(self):
        self._action = ast.Module(body=[self._args[0]], lineno=1)

        return self._action


class Identifier(AST):
    def eval(self):
        if self._args[1] == "load":
            self._action = ast.Name(id=self._args[0], ctx=ast.Load(), lineno=1)

        elif self._args[1] == "store":
            self._action = ast.Name(id=self._args[0], ctx=ast.Store(), lineno=1)

        return self._action


class FuncCall(AST):
    def eval(self):
        self._action = ast.Call(func=self._args[0], args=[self._args[1]], lineno=1)


class Assign(AST):
    def eval(self):
        self._action = ast.Assign(targets=[self._args[0]], value=self._args[1], lineno=1)
        return self._action


class Expression(AST):
    def eval(self):
        self._action = ast.Expression(value=self._args[0], lineno=1)
        return self._action


class PrintStmt(AST):
    def eval(self):
        self._action = ast.Name(id='print', ctx=ast.Load(), lineno=1)
        return self._action


class Constant(AST):
    def eval(self):
        self._action = ast.Constant(value=self._args[0], lineno=1)
        return self._action
