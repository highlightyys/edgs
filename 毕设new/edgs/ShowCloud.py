# -*- coding: utf-8 -*-
"""
Created on Mon May  6 13:21:19 2019

@author: Administrator
"""
import wx
class ShowCloud(wx.Dialog):
    def __init__(self,filename):
        #print('------------------')
        wx.Dialog.__init__(self,None,-1,'词云',size=(600,500))
        self.Centre()#设置窗口居中
        panel = wx.Panel(parent=self)
        
        #创建垂直方向box布局管理器
        vbox=wx.BoxSizer(wx.VERTICAL)
        
        self.bmp = wx.Bitmap('C:/EdmsData/pic/' + filename +'.gif', wx.BITMAP_TYPE_GIF)
        
        self.image = wx.StaticBitmap(panel, -1, self.bmp)#创建静态图片
        
        b1= wx.Button(panel,1,label='确定')
        self.Bind(wx.EVT_BUTTON,self.closewindow ,b1)
        vbox.Add(self.image,10,flag = wx.ALIGN_CENTER | wx.ALL,border=20)
        vbox.Add(b1,1,flag=wx.ALIGN_CENTER | wx.ALL ,border=20)
        panel.SetSizer(vbox)
          
    def closewindow(self,event):
        self.Close(True)

    
class App(wx.App):
    def OnInit(self):
        filename = '2009_2016年云南省医疗机构消毒灭菌效果趋势评价_李建云_周晓梅'
        #创建窗口对象
        Dialog = ShowCloud(filename)
        Dialog.Show()
        return True
    
    def OnExit(self):
        print('应用程序退出')
        return 0
    
#当前模块名是不是主模块，即应用程序的入口  
if __name__ == '__main__':
    app = App()#调用上面函数
    app.MainLoop()#进入主事件