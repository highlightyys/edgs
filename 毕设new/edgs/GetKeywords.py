# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 18:00:20 2019

@author: Administrator
"""
import jieba
import jieba.analyse
from MyDataFrame import MyDataFrame
class ToTFIDF(object):
    def get_keywords(self,filename):
        mdf = MyDataFrame()
        df = mdf.new_DataFrame()
        #jieba.analyse.extract_tags(df['content'][0])#list,关键词降序排列
        jieba.load_userdict('C:/TMdata/计算机词汇.txt')#导入自定义词典
        jieba.analyse.set_stop_words('C:/TMdata/stopwords.txt')
        
        
        for i in range(len(df)):
            if df['filename'][i] == filename:
                n = i
                #print(i)
        TFres = jieba.analyse.extract_tags(df['content'][n])
        return TFres #list
    
if __name__ == '__main__':
    filename = '2009_2016年云南省医疗机构消毒灭菌效果趋势评价_李建云_周晓梅'
    tfidf = ToTFIDF()
    TFres = tfidf.get_keywords(filename)
    keywords_str = ','.join(TFres[:5])
    print(keywords_str)#前五个关键词
    
    
    
    