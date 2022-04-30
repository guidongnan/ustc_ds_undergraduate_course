from linesearch import *




x0=np.array([-2,-1,0,1,2]).reshape(-1,1)
xk,min_v,k,W = newton(y,x0)
print("----------")
print("初始值为{}".format(x0))
print("最优解的值为{}".format(xk))
print("最小值为{}".format(min_v))
print("迭代次数为{}".format(k))