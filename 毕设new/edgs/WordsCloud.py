# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 17:59:54 2019

@author: Administrator
"""

import wordcloud
#import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from MyDataFrame import MyDataFrame

class WordsCloud(object):   
    
    def saveCloud(self,filename):
        mdf = MyDataFrame()
        df = mdf.new_DataFrame()
        df2 = mdf.m_cut(df)
        
        stoplist = list(pd.read_csv('C:/TMdata/stopwords.txt',names=['w'],sep='aaa',encoding='utf-8',engine='python').w)
        myfont=r'C:\Windows\Fonts\msyh.ttc'
        for i in range(len(df2)):
            if df2.filename[i] == filename:
                cloudobj = wordcloud.WordCloud(font_path = myfont, 
                width = 400, height = 300,
                mode = "RGBA", background_color = '#ffffff',
                stopwords = stoplist).generate(' '.join(df2['fenci'][i]))  
            #plt.imshow(cloudobj)
            #plt.axis("off")
            #plt.show()
                cloudobj.to_file('C:/EdmsData/pic/'+df2['filename'][i] + '.gif')
    

            
    def showCiyun(self,filename):
        im = Image.open('C:/EdmsData/pic/'+filename+'.gif')
        im.show()
               
if __name__ == '__main__':
    cy = WordsCloud()
    filename = '2009_2016年云南省医疗机构消毒灭菌效果趋势评价_李建云_周晓梅'
    cy.saveCloud(filename)
    cy.showCiyun(filename)
