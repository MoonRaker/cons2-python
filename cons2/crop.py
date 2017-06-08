# crop.py
# Derek Groenendyk
# 2/15/2017
# reads input data from Excel workbook

from collections import OrderedDict
import logging
import numpy as np
import os
import sys

from cons2.cu import CONSUMPTIVE_USE

# from utils import excel

logger = logging.getLogger('crop')
logger.setLevel(logging.DEBUG)

class CROP(object):
    """docstring for CROP"""
    def __init__(self, shrtname, longname, crop_type, mmnum, directory, sp):
        self.sname = shrtname
        self.lname = longname
        self.crop_type = crop_type
        self.directory = directory

        if self.crop_type == 'ANNUAL':
            self.mmnum = mmnum 

        if sp.et_method == 'fao':
            self.stages = {}
            self.kc = {}
            # self.read_cropdev()
            self.read_stages()
            self.read_kc()
        elif sp.et_method == 'scs':
            self.get_nckc()
            self.get_ckc()

        # methods = {
        # 'ANNUAL': ANNUAL,
        # 'PERENNIAL': PERENNIAL
        # }
        # self.cu = methods[crop_type](sp, self)              

        self.cu = CONSUMPTIVE_USE(sp, self)  


    def read_cropdev(self):
        try:
            infile = open(os.path.join(self.directory,'data','crop_dev_coef.csv'),'r')
        except TypeError:
            logger_fn.critical('crop_dev_coef.csv file not found.')
            raise
        lines = infile.readlines()
        infile.close()

        # sline = lines[1].split(',')
        # cname = sline[0].replace(' ','')
        # temp_cname = cname
 
        stage_flag = False
        kc_flag = False 
        switch = False
        i = 1
        # while i < len(lines):
        while i < len(lines):
            
            sline = lines[i].split(',')
            cname = sline[0].replace(' ','')             
            # print(cname,self.sname)

            if cname != '':
                if cname == self.sname:
                    # print(i)
                    if not switch:
                        stage = sline[1].lower()
                        self.stages[stage] = np.array([float(item) for item in sline[2:6]])
                        # print(1.0-np.sum(self.stages[stage]))
                        stage_flag = True
                    else:                                   
                        num = int(sline[1].replace(' ',''))
                        self.kc[num] = np.array([float(item) for item in sline[2:5]])
                        kc_flag = True

            else:
                if switch:
                    break
                i += 1
                switch = True

            i += 1                               

        if stage_flag == False or kc_flag == False:
            logger.critical('Crop, ' + self.sname + ', not found in crop_dev_coef.csv.') # include site??
            raise   

    def read_stages(self):
        try:
            infile = open(os.path.join(self.directory,'data','fao_crop_stages.csv'),'r')
        except TypeError:
            logger_fn.critical('fao_crop_stages.csv file not found.')
            raise
        lines = infile.readlines()
        infile.close()

        flag = False

        i = 1
        while i < len(lines):
            sline = lines[i].split(',')
            cname = sline[0].replace(' ','')             

            if cname != '':
                if cname == self.sname:
                    stage = sline[1].lower()
                    self.stages[stage] = np.array([float(item) for item in sline[2:6]])
                    flag = True
                else:
                    if flag:
                        break
                    flag = False

            i += 1                               

        if not flag:
            logger.critical('Crop, ' + self.sname + ', not found in fao_crop_stages.csv.') # include site??
            raise   

    def read_kc(self):
        try:
            infile = open(os.path.join(self.directory,'data','fao_crop_coef.csv'),'r')
        except TypeError:
            logger_fn.critical('fao_crop_coef.csv file not found.')
            raise
        lines = infile.readlines()
        infile.close()

        flag = False

        i = 1
        while i < len(lines):
            
            sline = lines[i].split(',')
            cname = sline[0].replace(' ','')   

            if cname != '':
                if cname == self.sname:                      
                    num = int(sline[1].replace(' ',''))
                    self.kc[num] = np.array([float(item) for item in sline[2:5]])
                    flag = True
                else:
                    if flag:
                        break
                    flag = False

            i += 1                               

        if not flag:
            logger.critical('Crop, ' + self.sname + ', not found in fao_crop_coef.csv.') # include site??
            raise               

    def get_nckc(self):
        """
        Reads in crop coefficients.

        Parameters
        ----------
        name: string
            Name of the crop

        Returns
        -------
        nckc: list
            List of crop coefficients
        """

        try:
            infile = open(os.path.join(self.directory,'data','scs_crop_stages.csv'),'r')
        except TypeError:
            logger.critical('scs_crop_stages.csv file not found.')
            raise
        lines = infile.readlines()
        infile.close()

        nckca = [float(item) for item in lines[0].split(',')[1:]]
        nckcp = [float(item) for item in lines[1].split(',')[1:]]

        if self.crop_type == 'PERENNIAL':
            self.nckc= nckcp
        else:
            self.nckc = nckca


    def get_ckc(self):
        """
        Reads in crop coefficients.

        Parameters
        ----------
        name: string
            Name of the crop

        Returns
        -------
        ckc: list
            List of crop coefficients
        """

        try:
            infile = open(os.path.join(self.directory,'data','scs_crop_coef.csv'),'r')
        except TypeError:
            logger_fn.critical('scs_crop_coef.csv file not found.')
            raise
        else:
            lines = infile.readlines()
            infile.close()

        if self.crop_type == 'PERENNIAL':
            end = 26
        else:
            end = 22

        for line in lines:
            sline = line.split(',')
            sline[-1] = sline[-1][:-1]
            # print(sline[0],self.sname)
            if sline[0] == self.sname:
                vals = [float(item) for item in sline[1:end]]
                self.ckc = vals
                break     

