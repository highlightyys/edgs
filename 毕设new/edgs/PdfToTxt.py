# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:17:30 2019

@author: Administrator
"""
#传入文件路径名，将所有pdf转为同名的txt文件保存

import sys
import importlib
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import os

class PdfToTxt(object):
    
    #从已知文件路径中读取pdf文件，并将其转化为同名txt文件

    def readPDF(path, toPath):
        # 以二进制形式打开pdf文件
   
        with open(path, "rb") as f:
            # 创建一个pdf文档分析器
            parser = PDFParser(f)
            # 创建pdf文档
            pdfFile = PDFDocument()
            # 链接分析器与文档对象
            parser.set_document(pdfFile)
            pdfFile.set_parser(parser)
            # 提供初始化密码
            pdfFile.initialize()
            # 检测文档是否提供txt转换
        if not pdfFile.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            # 解析数据
            # 数据管理
            manager = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(manager, laparams=laparams)
            # 解释器对象
            interpreter = PDFPageInterpreter(manager, device)
    
            # 开始循环处理，每次处理一页
            for page in pdfFile.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if(isinstance(x, LTTextBoxHorizontal)):
                        with open(toPath, 'a',encoding='utf-8') as f:
                            str = x.get_text()
                            # print(str)
                            f.write(str+"\n")

    #遍历文件夹及其子文件夹
    def list_all_files(rootdir):
        _files = []
        list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path = os.path.join(rootdir,list[i])
            if os.path.isdir(path):
                _files.extend(PdfToTxt.list_all_files(path))
            if os.path.isfile(path):
                _files.append(path)
        return _files
    #将传入的文件夹及其子文件夹下的pdf文件转为txt文件，并存到固定路径下
    def getpdf_list(pdf_path):
        txt_path =  'C:/EdmsData/txt0/'
        #清空txt文件中文件
        shanchu = os.listdir(txt_path)
        #print(shanchu)
        for i in range(len(shanchu)):
            os.remove(txt_path+shanchu[i])
        #--------------------------------
        all_list = PdfToTxt.list_all_files(pdf_path)
        path = ''
         
        txt_list=[]
        for onelist in all_list:
            if onelist.find('pdf') != -1:
                txt_list.append(onelist)
                
        print(txt_list)
        for i in range(len(txt_list)):
            path = txt_list[i]
            print(path)
            index = txt_list[i].rfind('\\')
            one_list = txt_list[i][index:-4]
            toPath = txt_path+one_list+'.txt'
            
            #print('------')
            #print(toPath)
            try:
                PdfToTxt.readPDF(path,toPath)
                #print('---------------------')
            except:
                print("error")
                continue
            
            
if __name__ == '__main__':
    pdf_path = 'C:/TMdata/PDF4'
    #将所有pdf转为同名的txt文件
    PdfToTxt.getpdf_list(pdf_path)
    