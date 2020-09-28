# -*- coding: utf-8 -*-
"""
Created on Sat May  4 20:06:33 2019

@author: Administrator
"""
from sklearn.externals import joblib
from MyDataFrame import MyDataFrame
class GetCatagory(object):
    def getAllTextCatagory(self):
        nbf =joblib.load('LR_model')  # 加载Logistic回归模型
        mdf = MyDataFrame()
        df = mdf.new_DataFrame()
        df2 = mdf.m_cut(df)
        rawfile=[]#空格分隔开的文本
        for i in range(len(df2)):
            rawfile.append(' '.join(df2['fenci'][i]))

        countvec=joblib.load('countvec_LR')  #加载Logistic回归模型拟合时的原始词频特征矩阵
        x_test_wordmtx = countvec.transform(rawfile) 
        transformer = joblib.load('transformer_LR')
        x_test = transformer.transform(x_test_wordmtx)
        catagory_list = nbf.predict(x_test) #对测试集进行类别预测，返回一个list
        #print(catagory_list)
        #print(type(catagory_list))
        return catagory_list
    
    """
    def getOneTextCatagory(self,filename):
        catagory_list = self.getAllTextCatagory()
    """ 
        
    
if __name__ == '__main__':
    gc = GetCatagory()
    catagory_list = gc.getAllTextCatagory()  # list
    print(catagory_list)