# -*- coding: utf-8 -*-
"""
Created on Sun May  5 18:12:03 2019

@author: Administrator
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import jieba
import networkx as nx 
from MyDataFrame import MyDataFrame

class GetAbstract(object):
    def readAbstract(self,filename):
        filepath = 'C:/EdmsData/txt/'+filename+'.txt'
        content = []
        recording = False
        with open(filepath,encoding='utf-8',errors='ignore') as f:
            for line in f:
                line = line.strip('\n')
                #print(line)
                if line.find('关键词') != -1:
                    #print('q')
                    break
                if line.find('摘 要') != -1 or line.find('摘要') != -1 or line.find('摘'+ '\n' +'要') != -1:#  or line.find('摘') != -1 :
                    #print('i')
                    recording = True
                if recording:
                    content.append(line)
                    #print(content)
        return ''.join(content)


    def generateAbstract(self,content):
        #1.形成数据框
        ga = GetAbstract()
        sentdf = pd.DataFrame(ga.cut_sentence(content))
        # 去除过短的句子，避免摘要出现无意义的内容
        sentdf['txtlen'] = sentdf[0].apply(len)#计算每个记录的长度
        #sentdf.head()
        sentlist = sentdf[0][sentdf.txtlen > 20]#选出长度大于20的
        print(len(sentlist))
        
        txtlist = [ " ".join(jieba.lcut(w)) for w in sentlist]
        vectorizer = CountVectorizer() 
        X = vectorizer.fit_transform(txtlist) # 将文本中的词语转换为词频矩阵
        tfidf_matrix = TfidfTransformer().fit_transform(X)  #转成TF-IDF矩阵
        
        similarity = nx.from_scipy_sparse_matrix(tfidf_matrix * tfidf_matrix.T)  #计算相应相似矩阵-----IF-IDF矩阵*它的转置，相当于提取出了特征根
        scores = nx.pagerank(similarity) 
        #print(scores) #每句话的一个pagerank评分
        #找出评分高的矩阵
        tops = sorted(scores.items(), key = lambda x: x[1], reverse = True)#排序
        print(tops)
      
        topn = 3  #3句话
        topsent = sorted(tops[:topn])
        abstract = ''
        for item in topsent:
            abstract = abstract + sentlist.iloc[item[0]] + '\n'
        abstract_str = abstract[:-3]
        
        return abstract_str
        
        

    def cut_sentence(self,intxt):  
        delimiters = frozenset('。！？')  #以这三个符号作为分句标识，集合
        buf = []  #缓冲list
        for ch in intxt:  
            buf.append(ch)  
            if delimiters.__contains__(ch):  
                yield ''.join(buf)  
                buf = []  
        if buf:  
            yield ''.join(buf)  
            
        
if __name__ == '__main__':
    ga = GetAbstract()
    abstract_contents = ga.readAbstract('_一带一路_背景下_国际投资_课_省略_路径探析_以广西民族师范学院为例_郑国富')
    print(abstract_contents)
    #mdf = MyDataFrame()
    #df = mdf.new_DataFrame()
    #abstract_contents2 = ga.generateAbstract(df.content[2])
    #print(abstract_contents2)
    
