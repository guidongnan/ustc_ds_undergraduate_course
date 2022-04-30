# 运筹学2021~2022年秋季学期期末考试

edit by  [gdn](https://github.com/guidongnan/ustc_ds_undergraduate_course)

## 1.解线性规划问题

$$
\min \frac{ex_1+fx_2+gx_3+h}{ax_1+bx_2+cx_3+d}\\
s.t. \quad ax_1+bx_2+cx_3+d>0\\\quad ix_1+jx_2+kx_3\le l\\\quad mx_1+nx_2+ox_3\le p
$$

（其中a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p均为给定的常数，笔者记不清具体的数值了。。。）

提示：令$t=ax_1+bx_2+cx_3+d,y_1=\frac{x_1}{t},\cdots$转换为线性规划问题并求解。

## 2.网络流规划

证明最小成本循环流问题的模型化能力与最小成本流问题等价。并证明后者可以转换为最大流问题。

## 3.无约束优化

证明利用Wolfe-Powell线搜索算法的BFGS算法的全局收敛性。

即：

1. 当迭代点有限时，有$\nabla f(x)=0$。
2. 当迭代点无限时，有$f(x^{(k+1)})-f(x^{(k)})\to0$或者$\nabla f(x^{(k)})\to 0$

## 4.约束优化问题-SQP

写出SQP问题的K-T条件，并证明其步长$d^{(k)}$为$L_1$罚函数的下降方向。

即：
$$
\min_{d\in\R^n} \quad \frac{1}{2}d^TB_kd+{g^{(k)}}^Td \\
s.t. \quad a_i^Td+c_i=0\quad i\in\mathcal{E}=\left\{ 1,\cdots,m_e\right\}\\
\quad\quad\quad\quad\quad a_i^Td+c_i\le0\quad i\in\mathcal{I}=\left\{ m_e+1,\cdots,m\right\}\\
$$
写出上述约束问题的K-T条件，其中$A(x)=(a_1(x),\cdots,a_m(x))^T=(\nabla c_1(x),\cdots,\nabla c_m(x))^T$,并证明$d^{(k)}$是如下$L_1$罚函数的下降方向。
$$
P(x,\sigma)=f(x)+\sigma \left( \sum_{i\in\mathcal{E}}{|c_i(x)|_1}+\sum_{i\in\mathcal{I}}{|c_i^{(-)}(x)|_1}\right)
$$

## 5. 约束优化问题-乘子罚函数

考虑等式约束问题：
$$
\min \quad f(x)\\
s.t. \quad c(x)=0
$$
其中$c(x)=(c_1(x),\cdots,c_m(x))^T$。定义增广Lagrange函数为
$$
P(x, \lambda, \sigma)=L(x, \lambda)+\frac{\sigma}{2}\|c(x)\|^{2}
$$
证明：

设$\overline{x}$是等式约束问题的可行解，且对某个$\overline{\lambda}$，满足$P(\overline{x},\overline{\lambda},\sigma)$的极小点二阶充分条件，则$\overline{x}$是该等式约束问题的严格局部最优解。

## 6.建模问题

对于空间中给定的点$p$，考虑一个空间曲面$\left\{x\in\R^3 |f(x)=0\right\}$，给出点$p$到空间曲面的最小值的最优化建模。并给出问题显式解的一阶近似和二阶近似。
