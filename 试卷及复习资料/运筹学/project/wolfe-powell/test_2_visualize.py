from linesearch import *

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pyplot as plt

fig = plt.figure()
ax = Axes3D(fig)
xx = np.arange(-2, 2, 0.1)
yy = np.arange(-2, 4, 0.1)
X, Y = np.meshgrid(xx, yy)  # 网格的创建，这个是关键
# print(X.shape,Y.shape)
Z=np.zeros((len(yy),len(xx)))
for i in range(len(yy)):
    for j in range(len(xx)):
        Z[i][j] = get_fun(y,np.array([X[i][j],Y[i][j]]).reshape(-1,1))

# print(Z)
plt.xlabel('x')
plt.ylabel('y')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')
# plt.show()


x0=np.array([-2,2]).reshape(-1,1)
xk,min_v,k,W = newton(y,x0)

res = np.zeros(len(W[0]))
for i in range(len(W[0])):
    res[i] = get_fun(y,np.array([W[0][i],W[1][i]]).reshape(-1,1))
    print(W[0][i],W[1][i],res[i])


ax.plot(W[0],W[1],res,c='black')

plt.show()