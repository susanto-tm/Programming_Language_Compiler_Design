"""
Mathematical Algorithms

The following is a library of mathematical algorithms used as built-in functions for the language.
Each algorithm is implemented in classes and executed when initialized.

CORDIC algorithm translated from C (Michael Bertrand)
"""

import math
from sympy import *
import re

math_funcs = {}  # contains precomputed setup holding objects to each algorithm
funcs = ['Trig', 'Calculus']


class MathFunc:
    def setup(self):
        pass


class Trig(MathFunc):
    def __init__(self):
        self.sin = None
        self.cos = None
        self.tan = None
        self.atan = None
        self.asin = None
        self.acos = None
        self.sinh = None
        self.cosh = None
        self.tanh = None

    def eval(self, param, inverse=False):
        # if inverse, param = [side1, side2] -- side1 / side2 : else, param = [angle, units]
        if not inverse:
            if param[1] == 'deg':
                param[0] *= math.pi / 180

            self.sin = math.sin(param[0])
            self.cos = math.cos(param[0])
            self.tan = math.tan(param[0])
            self.sinh = math.sinh(param[0])
            self.cosh = math.cosh(param[0])
            self.tanh = math.tanh(param[0])

        else:
            self.atan = math.atan2(param[0], param[1])
            self.asin = math.asin(param[0] / param[1])
            self.acos = math.acos(param[0] / param[1])


class Calculus(MathFunc):
    def __init__(self):
        self.__expr = None
        self.__symbol = None
        self.operation = None
        self.function = None

    def eval(self, expression, param, operation):
        self.__expr = sympify(re.sub(r'\^', r'**', expression))
        self.operation = operation

        if self.operation == 'def_int':
            self.__symbol = symbols(param[0])
            lower_bound = param[1]
            upper_bound = param[2]

            # Already contains
            self.function = integrate(self.__expr, (self.__symbol, lower_bound, upper_bound))

        elif self.operation == 'indef_int':
            self.__symbol = symbols(param)
            self.function = integrate(self.__expr, self.__symbol)


class Math:
    def __init__(self, action, param):
        self.action = action
        self.param = param

    def exec(self):
        if self.action == 'Trig-angle' or self.action == "Trig-inv":
            # Accepts action = 'Trig-angle', params = [angle, units] or action = 'Trig-inv', params = [side1, side2]
            func = math_funcs['Trig']
            inverse = False
            if self.action == 'Trig-inv':
                inverse = True
            func.eval([self.param[0], self.param[1]], inverse=inverse)
            return func
        elif self.action == 'def_int' or self.action == 'indef_int':
            # Accepts indef_int', params = [expression, (symbol, from, to)] or 'def_int', params = [expression, symbol]
            func = math_funcs['Calculus']
            if self.action == 'indef_int':
                func.eval(self.param[0], self.param[1], 'indef_int')

            elif self.action == 'def_int':
                func.eval(self.param[0], (self.param[1], self.param[2], self.param[3]), 'def_int')

            return func


def setup():
    import sys, inspect
    for cls in funcs:
        add_func = eval(cls + '()')
        add_func.setup()
        math_funcs[cls] = add_func
