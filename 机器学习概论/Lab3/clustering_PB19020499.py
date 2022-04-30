import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial.distance import squareform
from sklearn.metrics import davies_bouldin_score


def process_data(path):
    with open(path, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()

    res_list = []
    for line in lines:
        line = line[:-1]
        x, y = line.split(' ')
        x = float(x)
        y = float(y)
        res_list.append([x, y])

    return np.array(res_list)


def plot_pic2(x_list, y_list, center_points, cluster=None):

    print("共有{}个聚类中心".format(len(np.unique(cluster))))
    plt.scatter(x_list, y_list, s=2, c=cluster)
    plt.scatter(x_list[center_points], y_list[center_points], s=5, c='r')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Results with DPC')

    plt.show()


def plot_pic(x_list, y_list, cluster=None):
    # unique_values = np.unique(cluster)
    # # print(unique_values)
    # i = 0
    # dic = {}
    # for value in unique_values:
    #     dic[value] = i
    #     i += 1
    # for i in range(len(cluster)):
    #     cluster[i] = dic[cluster[i]]
    # print(cluster)
    plt.scatter(x_list, y_list, s=2, c=cluster)
    plt.xlabel('rho_i')
    plt.ylabel('delta_i')
    plt.title('Decision Graph for DPC')
    plt.show()


def get_rou(dist, dc):
    return np.count_nonzero(dist - dc < 0, axis=0)


def get_sigma(dist, rou):
    n = len(rou)
    res = []
    for i in range(n):
        temp = dist[i, rou - rou[i]>  0]
        if len(temp) > 0 :
            res.append(np.min(temp))
        else:
            # 最大密度点的情况
            res.append(np.max(dist[i]))

    return np.array(res)


def process1():
    path1 = './datasets/Aggregation.txt'
    res_list = process_data(path1)
    n = len(res_list)
    dist = pdist(res_list, metric='euclidean')
    dist = squareform(dist)

    rou = get_rou(dist, dc=3)
    sigma = get_sigma(dist, rou)
    plot_pic(rou, sigma)

    rou_threshold = 38
    sigma_threshold = 8

    temp1 = np.argwhere(rou - rou_threshold > 0)
    temp2 = np.argwhere(sigma - sigma_threshold > 0)
    center_points = np.intersect1d(temp1, temp2)

    ll = []
    d_threshold = 1
    for i in range(len(center_points)):
        for j in range(i + 1, len(center_points)):
            if dist[center_points[i], center_points[j]] < d_threshold:
                ll.append(j)

    center_points = np.delete(center_points, ll)

    cluster = []
    for i in range(n):
        cluster_i = center_points[np.argmin(dist[i, center_points])]
        cluster.append(cluster_i)

    cluster = np.array(cluster)
    plot_pic2(res_list[:, 0], res_list[:, 1], center_points, cluster)
    print("DBI指数为：{}".format(davies_bouldin_score(res_list, cluster)))


def process2():
    path2 = './datasets/D31.txt'
    res_list = process_data(path2)
    n = len(res_list)
    dist = pdist(res_list, metric='euclidean')
    dist = squareform(dist)

    rou = get_rou(dist, dc=1)
    sigma = get_sigma(dist, rou)
    plot_pic(rou, sigma)

    rou_threshold = 50
    sigma_threshold = 2

    temp1 = np.argwhere(rou - rou_threshold > 0)
    temp2 = np.argwhere(sigma - sigma_threshold > 0)
    center_points = np.intersect1d(temp1, temp2)

    ll = []
    d_threshold = 1
    for i in range(len(center_points)):
        for j in range(i + 1, len(center_points)):
            if dist[center_points[i], center_points[j]] < d_threshold:
                ll.append(j)

    center_points = np.delete(center_points, ll)


    cluster = []
    for i in range(n):
        cluster_i = center_points[np.argmin(dist[i, center_points])]
        cluster.append(cluster_i)

    cluster = np.array(cluster)
    plot_pic2(res_list[:, 0], res_list[:, 1], center_points, cluster)
    print("DBI指数为：{}".format(davies_bouldin_score(res_list, cluster)))


def process3():
    path3 = './datasets/R15.txt'
    res_list = process_data(path3)
    n = len(res_list)
    dist = pdist(res_list, metric='euclidean')
    dist = squareform(dist)

    rou = get_rou(dist, dc=0.5)
    sigma = get_sigma(dist, rou)
    plot_pic(rou, sigma)

    rou_threshold = 25
    sigma_threshold = 1

    temp1 = np.argwhere(rou - rou_threshold > 0)
    temp2 = np.argwhere(sigma - sigma_threshold > 0)
    center_points = np.intersect1d(temp1, temp2)

    ll = []
    d_threshold = 0.3
    for i in range(len(center_points)):
        for j in range(i + 1, len(center_points)):
            if dist[center_points[i], center_points[j]] < d_threshold:
                ll.append(j)

    center_points = np.delete(center_points, ll)

    cluster = []
    for i in range(n):
        cluster_i = center_points[np.argmin(dist[i, center_points])]
        cluster.append(cluster_i)

    cluster = np.array(cluster)
    # plot_pic(res_list[:, 0], res_list[:, 1], cluster)
    plot_pic2(res_list[:, 0], res_list[:, 1], center_points, cluster)
    print("DBI指数为：{}".format(davies_bouldin_score(res_list, cluster)))


if __name__ == "__main__":
    process1()
    process2()
    process3()