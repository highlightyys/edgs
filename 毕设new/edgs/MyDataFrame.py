# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 17:50:08 2019

@author: Administrator
"""
#读入txt文件夹内txt文件，完成分词，形成数据框
import os
import pandas as pd
import jieba

class MyDataFrame(object):
    def gettxt_list(self):
        path = "C:/EdmsData/txt"
        all_list = os.listdir(path)
    
        txt_list=[]
        for onelist in all_list:
            if onelist.find('txt') != -1:
                txt_list.append(onelist[0:-4])   
        #print(txt_list)
        return txt_list
    
    #获取文件内容列表
    def readtxt(self,filename):
        #读取一个txt文件，内容保存在str中
        f=open('C:/EdmsData/txt/'+filename+'.txt','r',encoding='utf-8',errors='ignore')
        str = ''
        for line in f.readlines():
            a = line.strip('\n')
            str = str + a
        #print(str)
        return str
    
    
        
    #，文件名+文件内容：data的list of list
    def getAlldata(self):
        filesdata = []
        mdf = MyDataFrame()
        txt_lists = mdf.gettxt_list()
        #print(txt_lists)
        for i in range(len(txt_lists)):
            filename = txt_lists[i]
            file_content = mdf.readtxt(filename)
            listi = [filename,file_content]
            filesdata.append(listi)
        #print(data)
        return filesdata
    
    #数据框df，两列，一列标题名，一列为txt内容

    def new_DataFrame(self): 
        mdf = MyDataFrame()
        filesdata= mdf.getAlldata()
        df_files = pd.DataFrame(data=filesdata,columns = ['filename','content'])
        return df_files
    
    #分词去停用词，返回一个新的数据框
    def m_cut(self,df):
        dict='C:/TMdata/计算机词汇.txt'
        jieba.load_userdict(dict)
        stoplist = list(pd.read_csv('C:/TMdata/stopwords.txt',names=['w'],sep='aaa',encoding='UTF-8',engine='python').w)
        list_fenci = []
        for i in range(len(df)):
            listi = [w for w in jieba.cut(df.content[i]) if w not in stoplist and len(w) >1]
            list_fenci.append(listi)
            
        df['fenci'] = list_fenci
        return df
    
    


if __name__ == '__main__':
    mdf = MyDataFrame()
    df = mdf.new_DataFrame()
    df2 = mdf.m_cut(df)
    print(df2)
    print(type(df2))