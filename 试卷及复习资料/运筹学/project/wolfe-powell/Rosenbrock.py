import numpy as np
from sympy import *

# 可自由定义
d=2

x_list=[]
for i in range(1,d+1):
    exec("x{} = symbols('x{}')".format(i,i),globals())
    exec("x_list.append(x{})".format(i))

y=0
for i in range(1,d):
    exec("y += (x{}-1)**2".format(i),globals())
    exec("y += 100*(x{}-x{}**2)**2".format(i+1,i),globals())