import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

train_path = str(sys.argv[1])
test_path = str(sys.argv[2])

with open(train_path,'r') as fp:
    train_data = fp.readlines()

with open(test_path,'r') as fp:
    test_data = fp.readlines()

item_list = []
for item in train_data:
    item = item[:-1]
    item = item.split(',')
    for i in range(len(item[2:])):
        try:
            item[i+2] = float(item[i+2])
        except:
            pass
    item_list.append(item)
df = pd.DataFrame(item_list)

df.replace(['M','B'],[0,1],inplace=True)
X = df.loc[:,2:]
y = df.loc[:,1]

item_list = []
for item in test_data:
    item = item[:-1]
    item = item.split(',')
    for i in range(len(item[2:])):
        try:
            item[i+2] = float(item[i+2])
        except:
            pass
    item_list.append(item)
df_test = pd.DataFrame(item_list)

X_test = df_test.loc[:,2:]
# y_test = df_test.loc[:,1]


class LogisticRegression():
    def __init__(self,dim):
        self.dim = dim
        self.w = np.mat(np.zeros((dim + 1,1)))

    def sigmoid(self,x):
        return 1.0 /(1.0 + np.exp((-1.0)*x))

    def normalization(self,X):
        #有些数据过大，进行正则化，进行正态分布的正则化
        m,n = X.shape
        for k in range(n):
            i = k + 2
            temp = X.loc[:,i]
            avg = np.average(temp)
            var = np.var(temp)
            X.loc[:,i] = (X.loc[:,i] - avg)/ var**0.5
        return X

    def gradient_decrease(self,X,y,alpha=0.01,epoch=1000,epsilon=1e-3):
        m,n = X.shape
        X = self.normalization(X)
        #添加“1”列，作为bias-b
        X = np.c_[X,np.ones((m,1))]
        loss_list = []
        for i in range(epoch):
            temp = np.zeros((n+1,1))
            loss = 0
            for j in range(m):#\partial{l(\beta)}/\partial{\beta}
                x_j = X[j].reshape(-1,1)
                output_j = np.dot(x_j.T,self.w)
                p1_j = 1.0 - self.sigmoid(-output_j)
                error_j = y[j] - p1_j
                loss += error_j**2
                temp_j = x_j * error_j
                temp += temp_j
            self.w = self.w + alpha*temp
            loss_list.append(float(loss))
            #提前停止标准，两次loss之差小于1e-4
            if(i>=2 and abs(loss_list[i]-loss_list[i-1])<epsilon):
                break
        return loss_list

    def fit(self,X):
        m, n = X.shape
        X = self.normalization(X)
        X = np.c_[X, np.ones((m, 1))]
        res_list = []
        for j in range(m):
            #计算输出结果并打印
            x_j = X[j].reshape(-1, 1)
            output_j = np.dot(x_j.T, self.w)
            p1_j = 1.0 - self.sigmoid(-output_j)
            if(p1_j > 0.5):
                print('B')
                res_list.append(1)
            else:
                print('M')
                res_list.append(0)
        return res_list


lr = LogisticRegression(X.shape[1])
loss_list = lr.gradient_decrease(X,y)
pred = lr.fit(X_test)