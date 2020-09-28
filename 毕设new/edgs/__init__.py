#
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 14:48:16 2019

@author: Administrator
"""

import wx
import wx.grid
import os
from data_info import GetData
from GetAbstract import GetAbstract
from MyDataFrame import MyDataFrame
from ShowAbstract import ShowAbstract
from WordsCloud import WordsCloud
from ShowCloud import ShowCloud
from OpenPDF import OpenPDF
from ShowPath import ShowPath

# 自定义窗口类MyFrame
class MyFrame(wx.Frame):
    column_names =['标题','类别','关键字' ]
    data=[['','','']]
    def __init__(self):
        super().__init__(parent=None, title='电子文献检索', size=(1000,700))
        self.Centre()  # 设置窗口居中
        self.panel = wx.Panel(self)
        self.SetBackgroundColour('#4DB3B3')
        #最底层box
        vbox0 = wx.BoxSizer(wx.VERTICAL)
        #上下两个box
        vbox1 = wx.BoxSizer()#水平
        vbox2 = wx.BoxSizer()#水平
        #1.在最底层添加标题       
        header_text = wx.StaticText(self.panel,label='电子文献检索系统',style=wx.TE_CENTER)
        font = wx.Font(18,wx.DEFAULT,wx.NORMAL,wx.NORMAL)
        header_text.SetFont(font)

        #2.在上层box添加内容
        openfiles_button = wx.Button(self.panel,id=1,label='打开')#打开文件夹
        openfiles_button.Bind(wx.EVT_BUTTON,self.OnOpen)       
        self.openfiles_text = wx.TextCtrl(self.panel,value='',style=wx.TE_LEFT)
        
        #搜索的文本框
        self.search_text = wx.TextCtrl(self.panel,value='',style=wx.TE_LEFT)
        search_button = wx.Button(self.panel,id=1,label='搜索')
        search_button.Bind(wx.EVT_BUTTON,self.SearchFiles)
     
        #3.向下层box添加内容   
        #下面box中的box
        vbox3 = wx.BoxSizer(wx.VERTICAL)#垂直
        vbox4 = wx.BoxSizer(wx.VERTICAL)       
        #网格
        
        self.grid = wx.grid.Grid(self.panel)
        self.grid.CreateGrid(len(self.data), len(self.data[0]))#行、列
        self.GridSetData(self.data,self.column_names)

        self.grid.SetColSize(0,330)
        self.grid.SetColSize(1,80)
        self.grid.SetColSize(2,240)
        
        # 设置行和列自定调整
        #self.grid.AutoSize()
        #绑定事件，当用户在行或列的标签区域敲击鼠标左键时触发该事件
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)  
        self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK,self.OnLableLeftDClick)
        
        self.path_show = wx.StaticText(self.panel,label='当前文件夹路径：')
               
        #下面右侧控件
        #分类下拉列表
        hbox5 = wx.BoxSizer()
        fenlei_text = wx.StaticText(self.panel,label='分类：')
        list1 = ['A_All','Computer', 'Art', 'Literature','Education','Philosophy','History','Space','Energy','Electronics','Communication','Mine','Transport','Enviornment','Agriculture','Economy','Law','Medical','Military','Politics','Sports']
        #ch1下拉列表，value为默认值，choices对应一个列表，style=wx.CB_SORT使选择列表中的元素按字母顺序显示。
        fenlei = wx.Choice(self.panel, -1, choices=list1, style=wx.CB_SORT)
        self.Bind(wx.EVT_CHOICE, self.on_choice, fenlei)#绑定事件
        
        #按钮      
        showpath_button = wx.Button(self.panel,label='查看路径')
        self.Bind(wx.EVT_BUTTON, self.showpath,showpath_button)
        
        #delete_button = wx.Button(self.panel,label='删除')
        #self.Bind(wx.EVT_BUTTON, self.deletefile,delete_button)
        #move_button = wx.Button(self.panel,label='移动')
        
        ciyun_button = wx.Button(self.panel,label='词云')
        self.Bind(wx.EVT_BUTTON, self.show_cloud,ciyun_button)
        abstract_button = wx.Button(self.panel,label='摘要')
        self.Bind(wx.EVT_BUTTON, self.get_abstract,abstract_button)
        #similar_button= wx.Button(self.panel,label='相似文档')
             
        #向上层box添加内容       
        #将打开文件夹添加到上层box
        vbox1.Add(openfiles_button,1,flag=wx.EXPAND)       
        vbox1.Add(self.openfiles_text,3,flag= wx.LEFT | wx.EXPAND,border=10)
        #将搜索框添加到上层box
        vbox1.Add(self.search_text,5,flag= wx.LEFT | wx.EXPAND,border=300)
        vbox1.Add(search_button,1,flag=wx.EXPAND | wx.LEFT, border=10)
        
        
        #想下层box添加内容
        vbox3.Add(self.path_show,1,flag=wx.EXPAND | wx.LEFT, border=10)
        vbox3.Add(self.grid,10,flag= wx.EXPAND)
        hbox5.Add(fenlei_text,1,flag=wx.EXPAND)
        hbox5.Add(fenlei,3,flag=wx.EXPAND)
        vbox4.Add(hbox5,flag= wx.EXPAND)
        vbox4.Add(showpath_button,flag= wx.EXPAND | wx.TOP,border = 150)
        #vbox4.Add(delete_button,flag= wx.EXPAND | wx.TOP,border = 30)
        #vbox4.Add(move_button,flag= wx.EXPAND | wx.TOP,border = 30)
        
        vbox4.Add(ciyun_button,flag= wx.EXPAND | wx.TOP,border = 30)
        vbox4.Add(abstract_button,flag= wx.EXPAND | wx.TOP, border = 30)
        #vbox4.Add(similar_button,flag= wx.EXPAND | wx.TOP, border = 20)
    
    
        #向下层box添加内容
        
        vbox2.Add(vbox3,5,flag= wx.EXPAND)
        vbox2.Add(vbox4,1,flag= wx.EXPAND | wx.ALL, border = 20)
        
     
        #向底层box添加内容       
        vbox0.Add(header_text,flag = wx.TOP | wx.EXPAND | wx.CENTER,border = 20) #将标题添加到底层box
        vbox0.Add(vbox1,1,flag=wx.ALL | wx.EXPAND,border=20)
        vbox0.Add(vbox2,10,flag=wx.ALL | wx.EXPAND,border=20)
        self.panel.SetSizer(vbox0)
        
    
    def GridSetData(self,data,column_names):
        #添加数据
        for row in range(len(data)):
            for col in range(len(data[row])):
                self.grid.SetColLabelValue(col, column_names[col])#设置列标题
                self.grid.SetCellValue(row, col, data[row][col])#设置单元格内容
                
                #SetRowLabelValue()，SetColLabelValue()和SetCellValue()，它们实际上设置显示在网格中的值
                #SetCellValue()方法要求一个行索引、一个列索引和一个值。而其它两个方法要求一个索引和一个值。
              
    def OnOpen(self,event):
        dlg = wx.DirDialog(None,message='打开文件夹',style=wx.DD_DEFAULT_STYLE)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.file = dlg.GetPath()          
            #print(self.file)#file为文件夹路径名
            self.openfiles_text.SetLabelText(self.file)# 在下方写入路径
            self.path_show.SetLabelText('当前文件夹路径：'+self.file)
            dlg.Destroy()

        #向后台传入路径file，获取data
        gd = GetData()
        self.data =[]
        self.data= gd.getInitData()
        #print(self.data)
        #print(len(self.data))
        
        self.grid.AppendRows(numRows = len(self.data) - 1)
        self.GridSetData(self.data,self.column_names)
        # 设置行和列自定调整
        #self.grid.AutoSize()
  
            
    def SearchFiles(self,event):
        str_search = self.search_text.GetValue()
        print(str_search)
        #print('搜索文件')
        gd = GetData()
        simfiles = gd.getSearchFiles(str_search)
        print(len(self.data)) #1.50
        print(len(simfiles))# computer 5
        print(simfiles)       
        if len(simfiles) == 0:
            nulldata = [['','','']]
            if len(self.data) == 1:
                self.data = nulldata
            else:               
                numrows = len(self.data) - 1 
                self.grid.DeleteRows(pos = 1,numRows = numrows)
                self.data = nulldata
        else:
            if len(self.data) > len(simfiles):    
                numrows = len(self.data) - len(simfiles) 
                self.grid.DeleteRows(pos = 1,numRows = numrows)
            elif len(self.data) < len(simfiles):
                numrows = len(simfiles) - len(self.data)
                self.grid.AppendRows(numRows = numrows)
            else:
                pass
            self.data = simfiles
        self.GridSetData(self.data,self.column_names)
        
      
    #网格点击事件
    def OnLabelLeftClick(self, event):
        print("RowIdx：{0}".format(event.GetRow()))#行索引
        self.rowidx = event.GetRow()
        print("ColIdx：{0}".format(event.GetCol()))#列索引
        #print(self.data[event.GetRow()])
        self.fileselect = self.data[event.GetRow()]
        print(self.fileselect)
        event.Skip()#确保还可以响应其他事件处理
 
    
    def OnLableLeftDClick(self,event):
        #print("RowIdx：{0}".format(event.GetRow()))#行索引
        #print("ColIdx：{0}".format(event.GetCol()))#列索引
        #print(self.data[event.GetRow()])
        self.fileselect = self.data[event.GetRow()]
        
        print(self.file) #文件夹路径
        #self.fileselect[0] 文件名
        
        allfiles =self.list_all_files(self.file) #所有文件，包含所在路径
        for i in range(len(allfiles)):
            if allfiles[i].find(self.fileselect[0]) != -1:
                filepath = allfiles[i]
                print(filepath)
                op = OpenPDF()
                op.experimentGuide(1,filepath)
                #os.popen(r'"C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe" filepath ')
    

    def get_abstract(self,event):
        try:
            filename = self.fileselect[0]
            print(filename)
            mdf = MyDataFrame()
            df = mdf.new_DataFrame()
            for i in range(len(df)):
                if df.filename[i] == filename:
                    file_content = df.content[i]

            #获取摘要
            ga = GetAbstract()
            abstract_contents = ga.readAbstract(filename)
            if len(abstract_contents) == 0:
                abstract_contents = ga.generateAbstract(file_content)
            else:
                pass
            print(abstract_contents)
            
            dialog = ShowAbstract(abstract_contents)
            dialog.Show()
            
        except:
            pass
    
    def showpath(self,event):       
        try:
            filename = self.fileselect[0]
            
            allfiles =self.list_all_files(self.file) #所有文件，包含所在路径
            for i in range(len(allfiles)):
                if allfiles[i].find(filename) != -1:
                    filepath = allfiles[i]
                    print(filepath)
            
            dialog = ShowPath(filepath)
            dialog.Show()
            
        except:
            pass
        
        

        #遍历文件夹及其子文件夹
    def list_all_files(self,rootdir):
        _files = []
        list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path = os.path.join(rootdir,list[i])
            if os.path.isdir(path):
                _files.extend(self.list_all_files(path))
            if os.path.isfile(path):
                _files.append(rootdir +'\\'+list[i])
        return _files
            
            
        
    def show_cloud(self,event):
        try:
            filename = self.fileselect[0]
            print(filename)
            wc = WordsCloud()
            wc.saveCloud(filename)
            sc = ShowCloud(filename)
            sc.Show()
        except:
            pass


    #分类按钮下拉选择
    def on_choice(self, event):
        print('选择 {0}'.format(event.GetString()))
        catagory_select = event.GetString()
        gd = GetData()
        catagory_data = gd.getCatagoryData(catagory_select)
        print(len(self.data)) #1.50
        print(len(catagory_data))# computer 5
        #print(self.data)
        print(catagory_data)
        if len(catagory_data) == 0:
            nulldata = [['','','']]
            if len(self.data) == 1:
                self.data = nulldata
            else:               
                numrows = len(self.data) - 1 
                self.grid.DeleteRows(pos = 1,numRows = numrows)
                self.data = nulldata
        else:
            if len(self.data) > len(catagory_data):    
                numrows = len(self.data) - len(catagory_data) 
                self.grid.DeleteRows(pos = 1,numRows = numrows)
            elif len(self.data) < len(catagory_data):
                numrows = len(catagory_data) - len(self.data)
                self.grid.AppendRows(numRows = numrows)
            else:
                pass
            self.data = catagory_data
        self.GridSetData(self.data,self.column_names)
        

class App(wx.App):

    def OnInit(self):
        # 创建窗口对象
        frame = MyFrame()
        frame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()  # 进入主事件循环

