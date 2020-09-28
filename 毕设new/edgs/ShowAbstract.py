# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:21:19 2019

@author: Administrator
"""
import wx
class ShowAbstract(wx.Dialog):
    def __init__(self,abstract_content):
        #print('------------------')
        wx.Dialog.__init__(self,None,-1,'摘要',size=(500,400))
        self.Centre()#设置窗口居中
        panel = wx.Panel(parent=self)
        
        #创建垂直方向box布局管理器
        vbox=wx.BoxSizer(wx.VERTICAL)
        
        
        self.tc = wx.TextCtrl(panel,style=wx.TE_MULTILINE)
        self.tc.SetValue(abstract_content)

        b1= wx.Button(panel,1,label='确定')
        self.Bind(wx.EVT_BUTTON,self.closewindow ,b1)
        vbox.Add(self.tc,10,flag = wx.ALIGN_CENTER | wx.ALL | wx.EXPAND,border=20)
        vbox.Add(b1,1,flag=wx.ALIGN_CENTER | wx.ALL ,border=20)
        panel.SetSizer(vbox)
          
    def closewindow(self,event):
        self.Close(True)

    
class App(wx.App):
    def OnInit(self):
        abstract_content = '11111111111111111111111111111'
        #创建窗口对象
        Dialog = ShowAbstract(abstract_content)
        Dialog.Show()
        return True
    
    def OnExit(self):
        print('应用程序退出')
        return 0
    
#当前模块名是不是主模块，即应用程序的入口  
if __name__ == '__main__':
    app = App()#调用上面函数
    app.MainLoop()#进入主事件