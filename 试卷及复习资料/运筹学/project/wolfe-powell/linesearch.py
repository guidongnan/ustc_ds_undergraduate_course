from sympy import *
import numpy as np
from Rosenbrock import x_list,y,d
from get_gradient import get_gfun
from get_hess import get_hess
from get_fun import get_fun

def judge(fai, fai0, fai1, p_fai0, p_fai1, xk, dk, y, rho, a1, sigma, a2, alpha):
    # print(fai,fai0 + rho*alpha*p_fai0)
    while fai > fai0 + rho*alpha*p_fai0:

        alpha_head = a1+0.5*(a1-alpha)**2*p_fai1/((fai1-fai)-(a1-alpha)*p_fai1)
        a2 = alpha
        alpha = alpha_head
        fai = get_fun(y,xk + alpha * dk)

    p_fai = np.dot(get_gfun(y,xk+alpha*dk).T, dk)[0][0]

    if p_fai< sigma*p_fai0:
        alpha_head = alpha - (a1-alpha)*p_fai/(p_fai1-p_fai)
        a1 = alpha
        alpha = alpha_head
        fai1=fai
        p_fai1 = p_fai
        return judge(fai, fai0, fai1, p_fai0, p_fai1, xk, dk, y, rho, a1, sigma, a2, alpha)
    else:
        return alpha

def wolfe_powell(y,xk,dk,max_value,rho = 0.1,sigma = 0.4):
    a1 = 0
    a2 = max_value
    fai0 = get_fun(y,xk)
    fai1 = fai0
    p_fai0 = np.dot(get_gfun(y,xk).T,dk)[0][0]
    p_fai1 = p_fai0

    alpha = (a1 + a2) / 2
    fai = get_fun(y,xk + alpha * dk)

    return judge(fai, fai0, fai1, p_fai0, p_fai1, xk, dk, y, rho, a1, sigma, a2, alpha)


def newton(y, x0):
    # 用牛顿法求解无约束问题
    # x0是初始点，fun，gfun和hess分别是目标函数值，梯度，海森矩阵的函数
    maxk = 500
    k = 0
    epsilon = 1e-5

    W = np.zeros((d, maxk))

    while k < maxk:
        W[:, k] = x0[:, 0]
        gk = get_gfun(y,x0)
        Gk = get_hess(y,x0)
        dk = -1.0 * np.linalg.solve(Gk, gk)
        if np.linalg.norm(dk) < epsilon:
            break

        alpha_k = wolfe_powell(y,x0,dk,2)
        print(alpha_k)
        x0 = x0 + alpha_k*dk
        k += 1

    W = W[:, 0:k + 1]  # 记录迭代点
    return x0, get_fun(y,x0), k, W
