# site.py
# Derek Groenendyk
# 5/10/2016
# reads input data from Excel workbook
"""

"""

import calendar as cal
from collections import OrderedDict
from datetime import date
from datetime import timedelta as td
import logging
import numpy as np
import os
import pandas as pd
import sys

import cons2.excel as excel
import cons2
from cons2.crop import CROP
from cons2.weather import WEATHER

logger = logging.getLogger('site')
logger.setLevel(logging.DEBUG)

# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

# cons2_dir = os.path.dirname(os.path.abspath(cons2.__file__))

cons2_dir = os.getcwd()


class SITE(object):
    """docstring for SITE"""
    def __init__(self, sws):
        self.sitews = sws

        self.import_crops()

        self.read_sitefile()

        if self.et_method == 'scs':
            # self.units = 'english'
            self.wx = WEATHER(self.wx_file, self.wx_location, units=self.units)
        elif self.et_method == 'fao':
            # self.units = 'metric'
            self.wx = WEATHER(self.wx_file, self.wx_location)

        if isinstance(self.wx.data, pd.DataFrame):
            self.read_cropfile()    

        self.pcu = np.zeros((len(self.yrs), 13))
        self.pre = np.zeros((len(self.yrs), 13))
        self.pcuirr = np.zeros((len(self.yrs), 13))


    def read_sitefile(self):

        self.site_name = self.sitews.Name

        rind = 3

        # print(self.sitews.Name)
        # self.sitews.Cells(2, 5).Delete(-4159) # delete and shift left
        # self.sitews.Cells(3, 5).Delete(-4159) # delete and shift left

        # self.sitews.Cells(rind, 7).Value = "2010"
        # self.sitews.Cells(rind, 8).Value = "2016"

        self.huc = self.sitews.Cells(rind, 2).Value
        self.county = self.sitews.Cells(rind, 3).Value
        self.state = self.sitews.Cells(rind, 4).Value
        # self.nout = int(self.sitews.Cells(rind, 5).Value)
        self.npre = int(self.sitews.Cells(rind, 5).Value)
        self.nbegyr = int(self.sitews.Cells(rind, 6).Value)
        self.nendyr = int(self.sitews.Cells(rind, 7).Value)
        self.apdep = float(self.sitews.Cells(rind, 8).Value)

        # self.sp['nbegyr'] = 2016
        # self.sp['nendyr'] = 2016 
        # self.sitews.Cells(rind, 7).Value = 2016
        # self.sitews.Cells(rind, 8).Value = 2016

        self.yrs = np.arange(int(self.nbegyr), \
                               int(self.nendyr) + 1)

        print(self.yrs)

        # rind += 1
        # [self.sitews.Rows(rind).EntireRow.Delete() for i in range(10)]

        # rind += 2
        # self.nts = int(self.sitews.Cells(rind, 2).Value)

        # rind += 1
        # self.wts = int(self.sitews.Cells(rind, 2).Value)

        # rind += 2
        # self.nps = int(self.sitews.Cells(rind, 2).Value)

        # rind += 1
        # self.wps = int(self.sitews.Cells(rind, 2).Value)     

        rind += 2
        self.wx_file = str(self.sitews.Cells(rind, 2).Value).strip()
        # self.sitews.Cells(rind, 2).Value = 'wx_azmet.xlsx'

        # self.sp['wx_file'] = "wx_azmet.xlsx"
        # self.sitews.Cells(rind, 2).Value = "wx_azmet.xlsx"

        rind += 1
        self.wx_location = str(self.sitews.Cells(rind, 2).Value).strip()

        rind += 1
        self.units = str(self.sitews.Cells(rind, 2).Value).strip()

        rind += 1
        self.crop_param_name = str(self.sitews.Cells(rind, 2).Value).strip().upper()

        # print(self.crop_param_name, self.wx_location, self.wx_file)

        rind += 1
        # self.sitews.Cells(rind, 2).Value = 'scs'
        # self.sitews.Cells(rind, 2).Value = 'fao'
        # self.sitews.Cells(rind, 1).Value = 'ET_method'
        self.et_method = str(self.sitews.Cells(rind, 2).Value).strip().lower()   


    def import_crops(self):
        try:
            infile = open(os.path.join(cons2_dir,'data','crop_ref.csv'),'r')
        except TypeError:
            logger_fn.critical('crop_ref.csv file not found.')
            raise
        lines = infile.readlines()
        infile.close()

        self.crop_dict = {}

        for line in lines[1:]:
            sline = line.split(',')
            shortname = sline[0].replace(' ','').strip(' ')
            longname = sline[1].strip(' ')
            crop_type = sline[2].strip(' ').upper()
            

            self.crop_dict[shortname] = {}
            self.crop_dict[shortname]['longname'] = longname
            self.crop_dict[shortname]['crop_type'] = crop_type
            
            if 'annual' in crop_type.lower():
                mmnum = int(float(sline[3].strip(' ')[:-1]))
                self.crop_dict[shortname]['mmnum'] = mmnum
            else:
                self.crop_dict[shortname]['mmnum'] = None


    def read_cropfile(self, vis=False):

        # if self.et_method == 'scs':
            # crop_param_filename = 'scs_crop_parameters_scs'
        # elif self.et_method == 'fao':
        crop_param_filename = self.et_method + '_crop_parameters'

        pathname = os.path.join(cons2_dir, 'data', crop_param_filename + '.xlsx')

        cp_ex = excel.Excel(pathname, vis)
        cwb = cp_ex.wb

        # print(self.crop_param_name)

        sheets = cwb.Worksheets
        try:
            ws = sheets(self.crop_param_name)
        except:
            logger.critical(self.site_name.upper() + ': Crop tab ' + \
                self.crop_param_name + ' missing in crop file')
            raise


        # ws.Rows(9).EntireRow.Delete()


        crop_list = []

        rind = 3

        crop_name = ws.Cells(rind, 1).Value
        while crop_name != None and crop_name != 'None':
            rind += 1
            # if self.et_method == 'fao':
            #     if 'vegetables' in crop_name.lower():
            #         crop_name = 'lettuce'

            # elif self.et_method == 'scs':              
            #     if 'wheat' in crop_name.lower():
            #         crop_name = 'wheatwntrfall'
            #     if 'barley' in crop_name.lower():
            #         crop_name = 'grainspr'
            #     if 'sorghum' in crop_name.lower():
            #         crop_name = 'beansdry'
            #     if 'vegetables' in crop_name.lower():
            #         crop_name = 'vgtblsm'                   


            # if 'hay' in crop_name.lower():
            #     crop_name = 'alfalfa'
            # if 'corn' in crop_name.lower():
            #     crop_name = 'corngrn'                    
            # if 'orchard' in crop_name.lower():
            #     crop_name = 'orchardnocov'                                       

                # ws.Cells(rind, 1).Value = crop_name.upper()
                
            crop_list.append(crop_name.replace(' ','').lower())
            crop_name = ws.Cells(rind, 1).Value

        if self.et_method == 'fao' and False:

            # [ws.Rows(rind).EntireRow.Insert() for i in range(4)]
            # ws.Columns(3).EntireColumn.Delete()
            # ws.Columns(3).EntireColumn.Delete()

            # data = [
            #     ['cabbage','cabbagefll',9,1,12,31,122],
            #     ['cabbage','cabbagewtr',1,1,4,30,120],
            #     ['melon','melonspr',4,1,7,31,122],
            #     ['melon','melonfll',7,1,10,31,123]
            # ]

            # for i in range(4):
            #     # ws.Cells(rind, 1).Value = shrtname.upper()
            #     # ws.Cells(rind, 2).Value = shrtname

            #     crop_list.append(data[i][0])
            #     ws.Cells(rind, 1).Value = data[i][0]
            #     ws.Cells(rind, 2).Value = data[i][1]         
            #     ws.Cells(rind, 3).Value = data[i][2]
            #     ws.Cells(rind, 4).Value = data[i][3]
            #     ws.Cells(rind, 5).Value = data[i][4]
            #     ws.Cells(rind, 6).Value = data[i][5]
            #     ws.Cells(rind, 7).Value = data[i][6]
            #     rind += 1

            [ws.Rows(rind).EntireRow.Insert() for i in range(2)]

            data = [
                ['lettuce','lettucefll',10,1,12,31,91,'typical',1],
                ['lettuce','lettucewtr',1,1,3,31,90,'typical',1],
            ]

            for i in range(len(data)):
                # ws.Cells(rind, 1).Value = shrtname.upper()
                # ws.Cells(rind, 2).Value = shrtname

                crop_list.append(data[i][0])
                ws.Cells(rind, 1).Value = data[i][0]
                ws.Cells(rind, 2).Value = data[i][1]         
                ws.Cells(rind, 3).Value = data[i][2]
                ws.Cells(rind, 4).Value = data[i][3]
                ws.Cells(rind, 5).Value = data[i][4]
                ws.Cells(rind, 6).Value = data[i][5]
                ws.Cells(rind, 7).Value = data[i][6]
                ws.Cells(rind, 8).Value = data[i][7]
                ws.Cells(rind, 9).Value = data[i][8]
                rind += 1                

        self.crops = []

        # ws.Cells(2, 8).Value = 'STYPE'
        # ws.Cells(2, 9).Value = 'KCNUM'
        # ws.Range('B2').Insert(-4161)
        # ws.Cells(2, 2).Value = 'Nickname'.upper()

        rind = 2
        for i in range(len(crop_list)):
            rind += 1

            shrtname = crop_list[i].lower()

            # if 'crucifers' in shrtname:
            #     ws.Cells(rind, 1).Value = 'cabbage'
            #     shrtname = 'cabbage'

            try:
                self.crop_dict[shrtname]
            except KeyError:
                logger.critical(self.site_name.upper() + ': Crop ' + \
                    shrtname + ' not listed in crop_ref.csv.')
                raise

            acrop = CROP(shrtname, self.crop_dict[shrtname]['longname'],
                        self.crop_dict[shrtname]['crop_type'],
                        self.crop_dict[shrtname]['mmnum'],
                        cons2_dir, self)

            # if acrop.crop_type == 'ANNUAL':
            #     acrop.mmnum = self.crop_dict[shrtname]['mmnum']

            # ws.Range(ws.Cells(rind, 2), ws.Cells(rind, 2)).Insert(-4161)
            # ws.Range('B2').Insert(-4161)

            # if shrtname not in ['cabbage', 'melon']:
            #     ws.Cells(rind, 1).Value = shrtname.upper()
            #     ws.Cells(rind, 2).Value = shrtname

    
            # if self.et_method == 'scs' and shrtname == 'vgtblsm':
            #     ws.Cells(rind, 2).Value = 'chili'            

            acrop.nickname = ws.Cells(rind, 2).Value.replace(' ','').lower()
            # acrop.ncrop = int(ws.Cells(rind, 3).Value)

            # if 'cabbagefll' in acrop.nickname:
            #     # ws.Cells(rind, 1).Value = 'cabbage'
            #     ws.Cells(rind, 2).Value = 'crucifersfll'

            # if 'cabbagewtr' in acrop.nickname:
            #     # ws.Cells(rind, 1).Value = 'cabbage'
            #     ws.Cells(rind, 2).Value = 'cruciferswtr'    

            
            if self.et_method == 'scs':
                offset = 2
                acrop.nbtemp = int(ws.Cells(rind, 3).Value)
                acrop.netemp = int(ws.Cells(rind, 4).Value)

            if self.et_method == 'fao':
                offset = 0              
                # ws.Cells(rind, 8).Value = 'typical'
                # if shrtname  == 'corngrn':
                #     ws.Cells(rind, 8).Value = 'long'

                # if shrtname in ['wheat', 'barley', 'alfalfa', 'sorghum']:
                #     ws.Cells(rind, 9).Value = 2
                # elif shrtname in ['corngrn']:
                #     ws.Cells(rind, 9).Value = 1
                # if shrtname in ['melon']:
                    # ws.Cells(rind, 9).Value = 2           

                acrop.stype = ws.Cells(rind, 8).Value.lower()
                acrop.kcnum = int(ws.Cells(rind, 9).Value)
      
            mbegmo = int(ws.Cells(rind, 3 + offset).Value)
            mbegda = int(ws.Cells(rind, 4 + offset).Value)
            # acrop.mendmo = int(ws.Cells(rind, 5 + offset).Value)
            # acrop.mendda = int(ws.Cells(rind, 6 + offset).Value)
            acrop.ngrows = int(ws.Cells(rind, 7 + offset).Value) - 1

            acrop.beg = []
            acrop.end = []
            acrop.mbegmo = []
            acrop.mbegda = []            
            acrop.mendmo = []
            acrop.mendda = []

            for ayr in self.yrs:
                beg_date = date(ayr, mbegmo, mbegda)
                end_date = beg_date + td(days=acrop.ngrows)

                acrop.mbegmo.append(mbegmo)
                acrop.mbegda.append(mbegda)
                acrop.mendmo.append(end_date.month)
                acrop.mendda.append(end_date.day)

                # Previously Used
                # acrop.beg.append(beg_date.timetuple().tm_yday)    
                # acrop.end.append(end_date.timetuple().tm_yday)                

                if cal.isleap(ayr):
                    if mbegmo > 2:
                        acrop.beg.append(beg_date.timetuple().tm_yday - 1)
                        acrop.end.append(end_date.timetuple().tm_yday - 1)    
                    else:
                        acrop.beg.append(beg_date.timetuple().tm_yday)
                        acrop.end.append(end_date.timetuple().tm_yday)                                             
                else:
                    acrop.beg.append(beg_date.timetuple().tm_yday)    
                    acrop.end.append(end_date.timetuple().tm_yday)

            self.crops.append(acrop)

        if self.et_method == 'scs':
            rind += 3
            self.pclite = [float(item.Value) for item in \
                ws.Range(ws.Cells(rind, 2), ws.Cells(rind, 13))] 

        elif self.et_method == 'fao':
            rind += 2

            # ws.Rows(rind).EntireRow.Delete()
            # ws.Rows(rind).EntireRow.Delete()

            # ws.Cells(rind, 1).Value = 'Latitude' 
            # ws.Cells(rind, 2).Value = 31.0

            self.latitude = float(ws.Cells(rind, 2).Value)

        cp_ex.close_workbook(0)
        # return crops, pclite, latitude                   