## Excel_Class.py
## Derek Groenendyk
## 5/23/2012
## creates an excel object for working with excel workbooks
"""



"""

from win32com.client import *
import os
import numpy as np



class Excel(object):

    def __init__(self, filename, vis=True, create=False):
        self.cwd = os.getcwd()
        self.filename = filename
        self.open()
        if not create:
            self.open_workbook(vis)
        else:
            self.create_workbook(vis)
        # self.open()
        self.excel.Visible = vis

        # return self.wb

        # win32com.client.GetObject(None, 'Excel.Application')        


    def open(self):
        self.excel = DispatchEx('Excel.Application')


    # def close(self):
    #     self.excel.Visible = True
    #     self.excel.Quit()
    #     del self.excel
        

    def setVis(self,boolean):
        self.excel.Visible = boolean


    # def set_wbvis(self, wb, state):
    #     wb.Windows(1).Visible = state


    def open_workbook(self, state=True):
        #opens the workbook
        # self.open()
        # for book in self.excel.Workbooks:
        #     if os.path.basename(filename) == book.Name:
        #         print('Workbook already open: ' + filename)
        #         return None

        self.wb = self.excel.Workbooks.Open(self.filename)
        self.wb.Windows(1).Visible = state

        # return wb

    def close_workbook(self, save_state=0):
        # print(wb.Name)
        # xl = GetObject(wb.FullName)
        self.wb.Close(save_state)
        self.excel.Quit()
        del self.excel


    def createSheet(self,workbook,name):
        #creates a new worksheet if it doesn't already exist
        for sheet in workbook.Sheets:
            if sheet.name == name:
                flag = True
                break
            else:
                flag = False
        if not flag:
            workbook.Worksheets.Add().Name = name


    def create_workbook(self, state=True):
        # creates the workbook if it doesn't already exist
        # self.open()
        try:
            self.wb = self.excel.Workbooks.Add()
            self.wb.SaveAs(self.filename)
        except:
            print('Book already exists')
        # else:
        #     return self.wb
