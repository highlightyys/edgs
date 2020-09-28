# -*- coding: utf-8 -*-
"""
Created on Mon May  6 19:13:26 2019

@author: Administrator
"""

import win32con
from win32comext.shell.shell import ShellExecuteEx
from win32comext.shell import shellcon
import time
import win32event


class OpenPDF(object):
    def experimentGuide(self,index,filepath):
        if(index == 1):
            #exePath = r'C:\Program Files (x86)\Foxit Software\Foxit Reader\FoxitReader.exe'
            #filepath = r'C:\Users\Administrator\Desktop\资料\师傅带徒弟学：Python图形用户界面编程wxPython视频课程\wxPython实战(中文版)\wxPython实战(中文版).pdf'
     
            # handle = win32api.ShellExecuteEx(0, 'open', filepath, '', '', 1)
            procInfo = ShellExecuteEx(nShow=win32con.SW_SHOWNORMAL,
                                      fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                      lpVerb='open',
                                      lpFile=filepath,
                                      lpParameters='')
            # handle = win32process.CreateProcess(exePath, filepath, None, None, 0, win32process.CREATE_NO_WINDOW, None, None, win32process.STARTUPINFO())
            #print('wait for end')
            #等待进程结束
            #print(win32event.WaitForSingleObject(procInfo['hProcess'], -1))
            #print(win32event.SetEvent(procInfo))
            #time.sleep(5)
            #print('close it')

if __name__ == '__main__':
    op = OpenPDF()
    filepath = r'C:\Users\Administrator\Desktop\资料\师傅带徒弟学：Python图形用户界面编程wxPython视频课程\wxPython实战(中文版)\wxPython实战(中文版).pdf'
    op.experimentGuide(1,filepath)
