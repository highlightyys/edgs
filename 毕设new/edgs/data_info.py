# -*- coding: utf-8 -*-
"""
Created on Sat May  4 17:15:04 2019

@author: Administrator
"""
from MyDataFrame import MyDataFrame
from GetCatagory import GetCatagory
from GetKeywords import ToTFIDF
from SearchFiles import BM25
import operator
import jieba
import pandas as pd
        
class GetData(object):
    data = []
    #df2 = pd.DataFrame()
    
    def setInitData(self):
        #标题
        
        mdf = MyDataFrame()
        df = mdf.new_DataFrame()
        df2 = mdf.m_cut(df)
        
        #类别
        gc = GetCatagory()
        catagory_list = gc.getAllTextCatagory()
        #关键词
        tfidf = ToTFIDF()
             
        for i in range(len(df)):
            filename = df.filename[i]
            catagory = catagory_list[i]
            keywords = tfidf.get_keywords(filename)   #list
            keywords_str = ','.join(keywords[:5])
            onedata = [filename,catagory,keywords_str]
            self.data.append(onedata)
            
    def getInitData(self):
        self.setInitData()
        return self.data
    
    def getCatagoryData(self,catagory):
        catagory_data =[]
        #print(catagory)
        if catagory == 'A_All':
            catagory_data = self.data
        else:
            #print('-------------------')
            for i in range(len(self.data)):
                #print(self.data[i])
                if self.data[i][1] == catagory:
                    catagory_data.append(self.data[i])
                           
        return catagory_data
        
     
    def getSearchFiles(self,str_search):
        mdf = MyDataFrame()
        df = mdf.new_DataFrame()
        df2 = mdf.m_cut(df)
        filelist=[]
        for i in range(len(df2)):
            filelist.append(df2['fenci'][i])
        
        
        s = BM25(filelist)
        #print(s.f)
        #print(s.idf)
        #print(s.simall(['医疗机构', '数据挖掘', '领域', '一带一路', '领域']))
        #print(type(s.simall(['医疗机构', '数据挖掘', '领域', '一带一路', '领域'])))
        
        #对str_search 进行分词去停用词处理
        str_search_list = jieba.lcut_for_search(str_search)
        
        scores = s.simall(str_search_list)
        #scores.sort()
        #print(scores)
        simfile_list = []
        for i in range(len(scores)):
            simfile_list.append((i,scores[i]))
            
        simfile_list.sort(key=operator.itemgetter(1),reverse=True)
        #print(simfile_list)
        
        simfiles =[]
        gc = GetCatagory()
        catagory_list = gc.getAllTextCatagory()
        tfidf = ToTFIDF()
        
        for i in range(len(simfile_list)):
            a,b = simfile_list[i]
            if b > 1.5:
                print(df2.filename[a] +":"+str(b))       
                filename = df2.filename[a]
                catagory = catagory_list[a]
                keywords = tfidf.get_keywords(filename)   #list
                keywords_str = ','.join(keywords[:5])
                simfiles.append([filename,catagory,keywords_str])
           
        return simfiles      
    
    
    def deleteOneFile(self,filename):
        if len(filename) != 0:
            for i in range(len(self.data)):
                #print(self.data[i])
                if self.data[i][0] == filename:
                    deletedata = self.data.pop(i)
                    print(deletedata)
                    print('delete OK')
        return self.data
                   
        
          
    
if __name__ == '__main__':
    
    gd = GetData()
    data = gd.getInitData()
    #print(data)
    
    catagory_data = gd.getCatagoryData('Computer')
    #print(catagory_data)
    str_search = "数据挖掘与计算机技术"
    simfiles = gd.getSearchFiles(str_search)
    print(simfiles)