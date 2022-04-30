import math

import numpy as np
import pandas as pd


class TreeNode:
    # 一个决策树结点的类
    def __init__(self, feature=None, value=None,
                 threshold=None, left_child=None,
                 right_child=None):
        # 决策树分类所用的特征
        self.feature = feature
        # 决策树分类特征的取值
        self.value = value
        # 决策树分类的阈值
        self.threshold = threshold
        # 决策树分类为true时的子节点，是一个TreeNode
        self.left_child = left_child
        # 决策树分类为false时的子节点，是一个TreeNode
        self.right_child = right_child


def get_loss(label, pred):
    #获得回归问题所对应的G和H
    G = -2 * (label - pred)
    H = 2 * pd.Series(np.ones(pred.shape))
    return G, H


class XgboostTree(TreeNode):

    def __init__(self, min_gain=0, min_size=10,
                 max_depth=3, lam=0, gamma=0):
        # 继承TreeNode类
        TreeNode.__init__(self)
        # 设置划分的最小增益值
        self.min_gain = min_gain
        # 设置划分截止的最小数据量
        self.min_size = min_size
        # 设置树的最大深度
        self.max_depth = max_depth
        # 设置超参数lambda和gamma
        self.lam = lam
        self.gamma = gamma

    def fit(self, data, label, pred):
        G, H = get_loss(label, pred)
        np_all = np.c_[data,label,pred,G,H]
        self.root = self.tree_build(np_all)

    def predict_value(self, treenode, data):
        # 这里的data是一行数据

        # treenode.value非空，是叶子结点，直接返回
        if treenode.value:
            return treenode.value

        # 选取划分属性
        data_feature = data[treenode.feature]
        # 根据阈值大小，在左右子树递归寻找
        if data_feature < treenode.threshold:
            return self.predict_value(treenode.left_child,data)
        else:
            return self.predict_value(treenode.right_child,data)

    def predict(self, data):
        n = data.shape[0]
        label = []

        for i in range(n):
            x = np.array(data.iloc[i,:])
            pred_x = self.predict_value(self.root,x)
            label.append(pred_x)

        return np.array(label)


    def tree_build(self, np_all, depth_now=1):
        '''
        采用递归方法建树，np_all是一个包含data,label,pred,G,H的大np数组
        '''
        max_gain = 0
        size_num = np_all.shape[0]
        att_num = np_all.shape[1] - 4

        # 不满足决策树停止标准，继续建树
        if size_num >= self.min_size and depth_now <= self.max_depth:
            for att in range(att_num):
                # 分别对数据的第att个属性排序，获得排序后新的np_all
                data_att = np_all[:, att]
                sort_att = np.lexsort(data_att.reshape(1,-1))
                np_all = np_all[sort_att]

                # 分别对不同属性的不同值进行划分，计算每次划分的增益
                unique_values = np.unique(np_all[:, att])
                for value in unique_values:
                    # 根据不同值选取划分点
                    split_i = np.searchsorted(np_all[:, att], value)

                    # 根据划分点计算左右G,H
                    G = sum(np_all[:, -2])
                    G_left = sum(np_all[:split_i, -2])
                    G_right = sum(np_all[split_i:, -2])
                    H = sum(np_all[:, -1])
                    H_left = sum(np_all[:split_i, -1])
                    H_right = sum(np_all[split_i:, -1])

                    # 如果划分有一类为空，跳过
                    if not (G_left and G_right and H_left and H_right):
                        continue

                    # 获取信息增益
                    obj1 = -0.5 * (G**2/(H+self.lam)) + self.gamma
                    obj2 = -0.5 * (G_left**2/(H_left+self.lam) + G_right**2/(H_right+self.lam)) + 2 * self.gamma
                    gain = obj1 - obj2

                    #获得最大信息增益，记录分割点和分类属性及阈值
                    if gain > max_gain:
                        max_gain = gain
                        split_point = split_i
                        feature = att
                        threshold = value
            print("建立第{}层，选取的特征是第{}列，分类阈值是{}，信息增益是{}".format(depth_now,feature,threshold,max_gain))

            # 根据最大收益递归划分建树
            if max_gain > self.min_gain:
                # 获得根据feature分类后的data
                data_feature = np_all[:, feature]
                sort_feature = np.lexsort(data_feature.reshape(1, -1))
                np_all = np_all[sort_feature]
                left_np_all = np_all[:split_point]
                right_np_all = np_all[split_point:]

                # 递归建树
                left_child = self.tree_build(left_np_all,depth_now+1)
                right_child = self.tree_build(right_np_all,depth_now+1)

                # 返回根节点
                return TreeNode(feature=feature,threshold=threshold,left_child=left_child, right_child=right_child)

        # 不建树，返回叶子结点，只有value有值
        else:
            G = sum(np_all[:,-2])
            H = sum(np_all[:,-1])

            # 根据所有该分类叶子结点的样本数据取均值作为value
            w_value = -(G/(H+self.lam))
            return TreeNode(value=w_value)


class Xgboost(XgboostTree):

    def __init__(self,trees_num=5):
        XgboostTree.__init__(self)
        self.trees_num = trees_num
        self.trees = []


    def fit(self,data, label):
        # 初始化预测全0
        pred = np.zeros(label.shape)
        # 建trees_num棵树
        for i in range(self.trees_num):
            print("-----正在建立第{}棵树-----".format(i+1))
            xgbt = XgboostTree()
            xgbt.fit(data, label, pred)
            print("-----第{}棵树建立完毕-----".format(i+1))

            # 下一次建树的输出为之前全部的预测结果之和
            pred = pred + xgbt.predict(data)

            #记录该树
            self.trees.append(xgbt)


    def predict(self,data):
        # 初始化pred
        pred = np.zeros(data.shape[0])

        # 根据fit记录的树，遍历每棵树输出结果
        for tree in self.trees:
            #最终的预测为trees_num棵树预测结果之和
            pred = pred + tree.predict(data)

        return pred


# 先处理数据
def process_data(path, size=1):
    # df = pd.DataFrame()
    with open(path, 'r', encoding='utf-8') as fp:
        line_list = fp.readlines()
    # print(line)
    df_list = []

    for line in line_list:
        item_list = line[:-1].split(', ')
        # print(item_list)
        for i in range(len(item_list)):
            item_list[i] = float(item_list[i])
        # print(item_list)
        df_list.append(item_list)

    df = pd.DataFrame(df_list)
    df = df.iloc[:int((df.shape[0]-1)*size), :]
    # print(df.shape)
    df_train = df.iloc[:, :df.shape[1] - 1]
    df_label = df[df.shape[1] - 1]
    # print(df_label)
    # print(df_train)
    return df_train, df_label



if __name__ == "__main__":
    train_path = './train.data'
    train_data, train_label = process_data(train_path, size=1)
    # from sklearn.model_selection import train_test_split
    # train_data,test_data,train_label,test_label = train_test_split(data,label,test_size=0.3)
    test_path = './ailerons.test'
    test_data, test_label = process_data(test_path, size=1)
    xgb = Xgboost(trees_num=5)
    xgb.fit(train_data, train_label)
    pred_test = xgb.predict(test_data)
    with open('./results.txt','w',encoding='utf-8') as fp:
        for i in range(len(pred_test)):
            fp.write(str(pred_test[i])+'\n')
    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(test_label,pred_test)
    print("RMSE的值为：{}".format(math.sqrt(mse)))
    var = np.var(test_label)
    R = 1 - mse/var
    print("R的值为：{}".format(R))
