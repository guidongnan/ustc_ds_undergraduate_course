import numpy as np
from sympy import *

def get_gfun(expression, position):
    length = len(position)
    position = position.flatten()
    gradient = np.zeros(length)
    # get the variables
    variables = list(expression.free_symbols)
    # construct the evaluation list
    value = [(variables[k], position[k]) for k in range(length)]
    for k in range(length):
        gradient[k] = expression.diff(variables[k]).subs(value)
    return np.array(gradient).reshape(-1,1)