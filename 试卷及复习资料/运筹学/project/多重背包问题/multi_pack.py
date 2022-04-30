"""
有 N 种物品和一个容量为 V 的背包。第 i 种物品最多有 p[i] 件可用，每件耗费的空间是 w[i]，价值是 v[i]。
求解将哪些物品装入背包可使这些物品的耗费的空间总和不超过背包容量，且价值总和最大。

- 基本思路
dp[i][j] 表示前i个物品放入容量为j的背包得到的最大价值
dp[i][j] = Max(dp[i - 1][j - k*w[i]] + k*v[i]), 0 ≤ k ≤ p[i], k*w[i] ≤ j ≤ V

"""


# 基本动态规划
import time

import numpy as np


def mul_pack_dp(V, w, v, p):
    n = len(w)
    dp = [[0] * (V + 1) for _ in range(n + 1)]
    min_cost = [[0] * (V + 1) for _ in range(n + 1)]

    # 采用自底向上的动态规划算法
    for i in range(1, n + 1):
        x = i - 1  # 第i件物品的索引
        for j in range(V + 1):
            for k in range(min(p[x], j // w[x]) + 1):
                if dp[i - 1][j - k * w[x]] + k * v[x] > dp[i][j]:
                    dp[i][j] = dp[i - 1][j - k * w[x]] + k * v[x]
                    min_cost[i][j] = k

    # print(dp[n][V])
    print_path(np.array(min_cost), V, n, w,v)
    # print()


def print_path(min_cost, V, n, w,v):

    k = n
    while min_cost[k][V] == 0:
        k = k - 1
        if k == 0:
            return

    # print("{}({}个)".format(k,min_cost[k][V]), end=' ')

    V = V - min_cost[k][V] * w[k - 1]
    min_cost[k] = [0] * min_cost.shape[1]

    return print_path(min_cost[:,:V+1], V, n, w,v)


def parse_data(path):
    with open(path, 'r') as fp:
        data = fp.readlines()

    # print(data)
    V = int(data[0][:-1])
    # n = int(data[1][:-1])
    w = [int(i) for i in data[2][:-1].split(',')]
    v = [int(i) for i in data[3][:-1].split(',')]
    p = [int(i) for i in data[4][:-1].split(',')]
    return V, w, v, p



