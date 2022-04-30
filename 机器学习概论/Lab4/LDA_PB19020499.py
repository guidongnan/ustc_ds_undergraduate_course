import numpy as np
import time
import codecs

import pandas as pd
import jieba.posseg as psg
import re

class LDA():

    def __init__(self, alpha=6, beta=0.01, iter=50, topics_num=8):
        self.alpha = alpha
        self.beta = beta
        # 最大迭代次数
        self.iter = iter
        # 所有doc的列表和停用词列表
        documents, stopwords = self.read_file()
        print("Reading file has finished!")
        # docs是二维列表，docs[i][j]是第i篇文章第j个单词的对应的编号
        # word2id是字典，记录关键字是单词，值为对应编号的转换关系
        # id2word是字典，记录关键字是编号，值为对应单词的转换关系
        self.docs, self.word2id, self.id2word = self.preprocessing(
            documents, stopwords)
        print("Preprocessing has finished!")
        # M是文章数量
        self.M = len(self.docs)
        # V是所有单词的数量
        self.V = len(self.word2id)
        # Z是二维列表，z[i][j]记录第i篇文章第j个单词的topic
        self.Z = []
        # K是topic数量
        self.K = topics_num
        # 初始化
        # nmk是array(M*K),nmk[m][k]表明第m篇文档中由k这个topic产生的单词计数
        self.nmk = np.zeros([self.M, self.K]) + self.alpha
        # nkv是array(K*V),nkv[k][v]表明第k个topic产生单词v的计数
        self.nkv = np.zeros([self.K, self.V]) + self.beta
        # nk是array(K),nk[k]表明第k个topic产生全部单词的计数
        self.nk = np.zeros([self.K]) + self.V * self.beta

    # 读取文件
    def read_file(self):
        # 读取停止词文件
        file = codecs.open('stop_dic/stopwords.dic', 'r', 'utf-8')
        stopwords = [line.strip() for line in file]
        file.close()

        # 读数据集
        file = pd.read_excel('data/data.xlsx')
        documents = file.content
        return list(documents), stopwords

    # 预处理(分词，去停用词，为每个word赋予一个编号，文档使用word编号的列表表示)
    def preprocessing(self,documents, stopwords):
        word2id = {}
        id2word = {}
        docs = []
        currentDocument = []
        currentWordId = 0

        flag_list = ['n','nz','vn']
        for document in documents:
            # 分词
            segList = psg.cut(document)
            for seg_word in segList:
                word = seg_word.word
                # 单词长度大于1，并且不包含数字和单词，并且不是停止词，并且词性符合要求
                if len(word) > 1 and not re.search('[0-9]', word) \
                    and word not in stopwords and not re.search('[a-z]', word) and not re.search('[A-Z]', word)\
                        and seg_word.flag in flag_list:
                    # word出现过，docs直接增加其编号
                    if word in word2id:
                        currentDocument.append(word2id[word])
                    else:
                        # 增加一个新的word-ID，加入docs
                        currentDocument.append(currentWordId)
                        # 记录word->id的对应关系
                        word2id[word] = currentWordId
                        # 记录id->word的对应关系
                        id2word[currentWordId] = word
                        # 准备下一个word-ID
                        currentWordId += 1
            docs.append(currentDocument)
            currentDocument = []
        return docs, word2id, id2word

    # 进行初始化的多项分布的分配
    def multinomial(self):
        for d, doc in enumerate(self.docs):
            # d是文档的序号，doc是文档内容相应单词的编号
            zCurrentDoc = []
            for w in doc:
                pz = np.divide(np.multiply(
                    self.nmk[d, :], self.nkv[:, w]), self.nk)
                z = np.random.multinomial(1, pz / pz.sum()).argmax()
                zCurrentDoc.append(z)
                self.nmk[d, z] += 1
                self.nkv[z, w] += 1
                self.nk[z] += 1
            self.Z.append(zCurrentDoc)

    # gibbs采样
    def gibbsSampling(self):
        # 为每个文档中的每个单词重新采样topic
        for d, doc in enumerate(self.docs):
            for index, w in enumerate(doc):
                z = self.Z[d][index]
                # 将当前文档当前单词原topic相关计数减去1
                self.nmk[d, z] -= 1
                self.nkv[z, w] -= 1
                self.nk[z] -= 1
                # 重新计算当前文档当前单词属于每个topic的概率
                pz = np.divide(np.multiply(
                    self.nmk[d, :], self.nkv[:, w]), self.nk)
                # 按照计算出的分布进行采样
                z = np.random.multinomial(1, pz / pz.sum()).argmax()
                self.Z[d][index] = z
                # 将当前文档当前单词新采样的topic相关计数加上1
                self.nmk[d, z] += 1
                self.nkv[z, w] += 1
                self.nk[z] += 1
        return

    def perplexity(self):
        self.nd = np.sum(self.nmk, 1)
        n = 0
        ll = 0.0
        for d, doc in enumerate(self.docs):
            for w in doc:
                ll = ll + \
                    np.log(((self.nkv[:, w] / self.nk) *
                           (self.nmk[d, :] / self.nd[d])).sum())
                n = n + 1
        return np.exp(ll/(-n))

    def run(self):
        self.multinomial()
        # 记录匹配度
        self.perplexity_score = []
        for i in range(0, self.iter):
            self.gibbsSampling()
            self.perplexity_score.append(self.perplexity())
            # 打印iter信息
            print(time.strftime('%X'), "Iteration: ", i, " Completed"," Perplexity: ", self.perplexity_score[-1])
            if i < 10:
                continue
            # 如果匹配度小于前十次的平均值，停止迭代
            if self.perplexity_score[-1] > np.average(self.perplexity_score[-10:]):
                break

    def get_topic(self, maxTopicWordsNum=10):
        topicwords = []
        for z in range(0, self.K):
            # 对于每个主题，对在该主题下出现单词的数量排序
            ids = self.nkv[z, :].argsort()
            topicword = []
            # 根据id->word的转换关系转为id
            for j in ids:
                topicword.insert(0, self.id2word[j])
            # 返回需求的每个主题的相应数量的单词
            topicwords.append(topicword[0: maxTopicWordsNum])
        return topicwords


lda = LDA(alpha=5,beta=0.1)
lda.run()
print(lda.get_topic(maxTopicWordsNum=15))
