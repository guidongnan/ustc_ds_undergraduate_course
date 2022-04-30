import numpy as np
from sympy import *

def get_fun(expression, position):
    length = len(position)
    position = position.flatten()
    # get the variables
    variables = list(expression.free_symbols)
    # construct the evaluation list
    value = [(variables[k], position[k]) for k in range(length)]
    res = expression.subs(value)
    return res

# x1 = symbols('x1')
# x2 = symbols('x2')
# y = x1**2 + x2**2
#
# print(get_fun(y,[1,2]))
