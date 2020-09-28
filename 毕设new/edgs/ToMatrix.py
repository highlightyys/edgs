# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 15:30:51 2019

@author: Administrator
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from gensim import corpora,models
from MyDataFrame import MyDataFrame

class ToMatrix(object):
    
    #用sklearns生成文档-词条矩阵
    mdf = MyDataFrame()
    df = mdf.new_DataFrame()
    df2 = mdf.m_cut(df)
    
    
    #词频矩阵
    def tocountvec(self):
        rawfile=[]#空格分隔开的文本
        for i in range(len(ToMatrix.df2)):
            rawfile.append(' '.join(ToMatrix.df2['fenci'][i]))
        #print(rawfile) 
        #rawfile listoflist ,每一项为用空格连接的一篇文档
        countvec = CountVectorizer(min_df = 10)#最小词频
        res = countvec.fit_transform(rawfile)
        res#稀疏矩阵
        res.todense()#转置，仍为矩阵
        countvec.get_feature_names()#词汇列表，即每列对应的词条
        return res

    #tfidf矩阵    
    def totfidf(self):
        transformer = TfidfTransformer()
        tm = ToMatrix()
        X = tm.tocountvec()
        tfidf = transformer.fit_transform(X)
        #基于词频矩阵X计算TF-IDF值
        tfidf#31*241的矩阵
        return tfidf
        
        
    #gensim实现
    def tocorpus_tfidf(self):
        filelist=[]#空格分隔开的文本
        for i in range(len(ToMatrix.df2)):
            filelist.append(ToMatrix.df2['fenci'][i])
        dictionary = corpora.Dictionary(filelist)
        corpus = [dictionary.doc2bow(text) for text in filelist]
        corpus#语料库，list of list 
        
        tfidf_model = models.TfidfModel(corpus)#建立TF-IDF模型
        corpus_tfidf = tfidf_model[corpus]#对所需文档计算TF-IDF结果
        return corpus_tfidf
        
        
        
        
        
        
        
        
        
        
        
        