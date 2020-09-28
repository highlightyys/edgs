# -*- coding: utf-8 -*-
"""
Created on Wed May 15 20:55:14 2019

@author: Administrator
"""

import wx
class ShowPath(wx.Dialog):
    def __init__(self,filepath):
        #print('------------------')
        wx.Dialog.__init__(self,None,-1,'所在路径',size=(400,300))
        self.Centre()#设置窗口居中
        panel = wx.Panel(parent=self)
        
        #创建垂直方向box布局管理器
        vbox=wx.BoxSizer(wx.VERTICAL)
        
        self.tc = wx.TextCtrl(panel,style=wx.TE_MULTILINE)
        self.tc.SetValue(filepath)

        b1= wx.Button(panel,1,label='确定')
        self.Bind(wx.EVT_BUTTON,self.closewindow ,b1)
        vbox.Add(self.tc,10,flag = wx.ALIGN_CENTER | wx.ALL | wx.EXPAND,border=20)
        vbox.Add(b1,1,flag=wx.ALIGN_CENTER | wx.ALL ,border=10)
        panel.SetSizer(vbox)
          
    def closewindow(self,event):
        self.Close(True)

    
class App(wx.App):
    def OnInit(self):
        filepath = '2009_2016年云南省医疗机构消毒灭菌效果趋势评价_李建云_周晓梅'
        #创建窗口对象
        Dialog = ShowPath(filepath)
        Dialog.Show()
        return True
    
    def OnExit(self):
        print('应用程序退出')
        return 0
    
#当前模块名是不是主模块，即应用程序的入口  
if __name__ == '__main__':
    app = App()#调用上面函数
    app.MainLoop()#进入主事件