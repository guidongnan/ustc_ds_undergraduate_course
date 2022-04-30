import numpy as np
from sympy import *

def get_hess(expression, position):
    length = len(position)
    position = position.flatten()
    hess = np.zeros((length,length))
    # get the variables
    variables = list(expression.free_symbols)
    # construct the evaluation list
    value = [(variables[k], position[k]) for k in range(length)]
    for k in range(length):
        for j in range(length):
            hess[k][j] = expression.diff(variables[k],variables[j]).subs(value)
    return np.matrix(hess)