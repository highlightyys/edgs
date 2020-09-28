# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 17:16:40 2019

@author: Administrator
"""
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfTransformer
from gensim import corpora, models
from sklearn.feature_extraction.text import CountVectorizer
#先弄出文档词频矩阵，然后进行相应的模型训练
from MyDataFrame import MyDataFrame

class ToLDA(object):
    #1.主题模型的sklearn实现
    
    def skl_ldamodel(self):
        
        mdf = MyDataFrame()
        df = mdf.new_DataFrame()
        df2 = mdf.m_cut(df)
        rawfile=[]#空格分隔开的文本
        for i in range(len(df2)):
            rawfile.append(' '.join(df2['fenci'][i]))
        #print(rawfile) 
        #rawfile listoflist ,每一项为用空格连接的一篇文档
        countvec = CountVectorizer(min_df = 5)#最小词频
        X = countvec.fit_transform(rawfile)#稀疏矩阵
        
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(X)
        #设定LDA模型
        n_topics=10#提取主题个数
        ldamodel = LatentDirichletAllocation(n_components= n_topics)
        #拟合LDA模型
        ldamodel.fit(tfidf)
        #拟合后的模型实质
        print(ldamodel.components_.shape)#(10,705)
        ldamodel.components_[:2]#前两条，每个主题中每个词条出现的概率

        n_top_words = 10
        tf_feature_names = countvec.get_feature_names()
        ToLDA.print_top_words(ldamodel, tf_feature_names, n_top_words)
    
    #打印主题词
    def print_top_words(model,feature_names,n_top_words):
        for topic_idx,topic in enumerate(model.components_):
            print('Topic #%d:'% topic_idx)
            print(' '.join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()


    #2.主题模型的gensim实现
    def gen_ldamodel(self):
        mdf = MyDataFrame()
        df = mdf.new_DataFrame()
        df2 = mdf.m_cut(df)
        filelist=[]
        for i in range(len(df2)):
            filelist.append(df2['fenci'][i])
        #生成文档对应的字典和bow稀疏矩阵
        
        dictionary = corpora.Dictionary(filelist)  
        corpus = [dictionary.doc2bow(text) for text in filelist] # 仍为list in list  
        
        tfidf_model = models.TfidfModel(corpus) # 建立TF-IDF模型  
        corpus_tfidf = tfidf_model[corpus] # 对所需文档计算TF-IDF结果
        corpus_tfidf
        
        #拟合LDA模型
        from gensim.models.ldamodel import LdaModel
        # 列出所消耗的时间备查
        ldamodel = LdaModel(corpus, id2word = dictionary, num_topics = 10, passes = 10) 
        #列出最重要的若干个主题
        ldamodel.print_topics(num_topics = 20,num_words = 10)
        
        #计算各语料的LDA模型值
        corpus_lda = ldamodel[corpus_tfidf] # 此处应当使用和模型训练时相同类型的矩阵
        for doc in corpus_lda:
            print(doc)
        ldamodel.get_topics()#list of list 每个主题中每个词所对应的一个概率矩阵
        
        # 检索和文本内容最接近的主题
         # 检索和0.txt最接近的主题
        query_bow = dictionary.doc2bow(df2['fenci'][0]) # 频数向量
        query_tfidf = tfidf_model[query_bow] # TF-IDF向量
        print("转换后：", query_tfidf[:10])
        ldamodel.get_document_topics(query_bow) # 需要输入和文档对应的bow向量
        # 检索和文本内容最接近的主题       
        ldamodel[query_tfidf] #list，最接近的主题list


       
if __name__ == '__main__':
    tolda = ToLDA()
    tolda.skl_ldamodel()     
        
    tolda.gen_ldamodel()