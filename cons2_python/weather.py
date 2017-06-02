# weather.py
# Derek Groenendyk
# 5/4/2016
# weather class for cons2
"""


"""

from datetime import date
from datetime import datetime as dt
from itertools import islice
import logging
import numpy as np
import os
import pandas as pd
from pandas.tseries.offsets import MonthEnd,timedelta
import sys

import cons2.excel as excel


logger = logging.getLogger('weather')
logger.setLevel(logging.DEBUG)

# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)


class WEATHER(object):
    """docstring for WEATHER"""
    def __init__(self, fname, wsname, units='metric'):
        self.fname = fname
        self.wsname = wsname
        # self.numyrs = numyrs
        self.units = units

        # logger.debug(os.path.splitext(self.fname)[1])
        # logger.debug(os.getcwd())

        try:
            infile = open(self.fname,'r')
            infile.close()
        except TypeError:
            logger.critical('Cannot find weather file, ' + self.fname)
            raise           
        else:
            self.read_data()


    def read_data(self, vis=False):

        if os.path.splitext(self.fname)[1] == '.dat':
            dates = []
            wx = {}
            wx['temperature'] = []
            wx['precip'] = []

            with open(self.fname, 'r') as f:
                while True:
                    line = list(islice(f, 1))
                    if not line:
                        break
                    sline = line[0].split(',')
                    m = int(sline[1])
                    month = [31,28,31,30,31,30,31,31,30,31,30,31]
                    adate = dt(int(sline[0]), m, month[m - 1])
                    dates.append(adate)
                    wx['temperature'].append(float(sline[2]))
                    wx['precip'].append(float(sline[3]))

            self.data = pd.DataFrame(wx, index=dates)

        if os.path.splitext(self.fname)[1] == '.xlsx':
            # ex = excel.Excel(True)
            # wb = ex.open_workbook(os.path.join(os.getcwd(), self.fname), True)
            wb = excel.Excel(os.path.join(os.getcwd(), self.fname), vis).wb
            if wb == None:
                logger.critical('Close workbook: '+os.path.basename(self.fname))
                raise SystemExit

            # print(os.path.join(os.getcwd(), self.fname))

            self.data = None

            sheets = wb.Worksheets
            try:
                ws = sheets(self.wsname)
            except:
                logger.warn(self.wsname.upper() + ': Location tab missing in weather file')
            else:
                rind = 2
                numrows = 0
                year = ws.Cells(rind, 1).Value
                while year != None and year != 'None':
                    numrows += 1
                    rind += 1
                    year = ws.Cells(rind, 1).Value

                dates = []
                wx = {}
                # if 'prism' in self.fname.lower():
                #     wx['temp_min'] = np.zeros(numrows)
                #     wx['temp_max'] = np.zeros(numrows)
                #     wx['temp_avg'] = np.zeros(numrows)
                #     wx['precipitation'] = np.zeros(numrows)
                #     wx['dewpoint'] = np.zeros(numrows)   
                # else:
                #     wx['temperature'] = np.zeros(numrows)
                #     wx['precipitation'] = np.zeros(numrows)
                #     wx['wind'] = np.zeros(numrows)
                #     wx['radiation'] = np.zeros(numrows)           
                 

                # raise IndexError('Missing Index') 

                for row in range(numrows):
                    rind = row + 2
                    try:
                        m = int(ws.Cells(rind, 2).Value)
                    except:
                        if m == 12:
                            logger.critical(self.wsname.upper() + ': Missing weather\
                                data for year: ' + str(year + 1))
                        else:
                            logger.critical(self.wsname.upper() + ': Missing weather\
                             data for year: ' + str(year))
                        raise
                    else:
                        year = int(ws.Cells(rind, 1).Value)
                        month = [31,28,31,30,31,30,31,31,30,31,30,31]
                        adate = dt(year, m, month[m - 1])
                        dates.append(adate)

                        headers = []
                        for acol in range(ws.UsedRange.Columns.Count - 2):
                            col_name = ws.Cells(1, acol + 3).Value
                            if ws.Cells(1, acol + 3).Value != None:
                                headers.append(ws.Cells(1, acol + 3).Value.lower())

                        for hind in range(len(headers)):
                            aheader = headers[hind]
                            cind = hind + 3
                            if self.units == 'metric':
                                factor = 1.0
                            else:
                                if 'precipitation' in aheader:
                                    factor = 0.0393701
                                elif aheader in ['temp_min', 'temp_max', 'temp_avg', 'dewpoint']:
                                    factor = 9.0/5.0 + 32.0
                                elif 'wind' in aheader:
                                    factor = 2.237
                                elif 'radiation' in aheader:
                                    factor = 23.89

                            if rind == 2:
                                wx[aheader] = np.zeros(numrows)                       
                            wx[aheader][row] = float(ws.Cells(rind, cind).Value)*factor                 

                self.data = pd.DataFrame(wx, index=dates)

            wb.Close(0)


        elif os.path.splitext(self.fname)[1] == '.azmet':
            headers = ['air_temp_max',
                       'air_temp_min',
                       'air_temp_mean',
                       'rel_hum_max',
                       'rel_hum_min',
                       'rel_hum_mean',
                       'vpd_mean',
                       'sol_rad',
                       'precip',
                       '4in_soil_temp_max',
                       '4in_soil_temp_min',
                       '4in_soil_temp_mean',
                       '20in_soil_temp_max',
                       '20in_soil_temp_min',
                       '20in_soil_temp_mean',
                       'wind_speed',
                       'wind_mag',
                       'wind_dir',
                       'wind_dir_sd',
                       'max_windspd',
                       'heat_units',
                       'ref_et',
                       'ref_et_pen',
                       'act_vap_pressure',
                       'dewpoint']
            dates = []
            with open(self.fname, 'r') as f:
                while True:
                    line = list(islice(f, 1))
                    if not line:
                        break
                    sline = line[0].split(',')

                    ordinal = date.toordinal(date(int(sline[0]), 1, 1)) \
                        + int(sline[1]) - 1

                    temp_date = date.fromordinal(ordinal).timetuple()[:3]
                    adate = pd.Timestamp(date(*temp_date))
                    dates.append(adate)
                    wx_data = np.array([float(item) for item in sline[3:]])
                    idx = np.nonzero(wx_data == 999.0)[0]
                    wx_data[idx] = np.nan
                    wx_data = list(np.nan_to_num(wx_data))
                    if len(dates) == 1:
                        wx_data = [[item] for item in wx_data]
                        wx = dict(zip(headers, wx_data))
                    else:
                        for i in range(len(headers)):
                            wx[headers[i]].append(wx_data[i])

            logger.info('Finished reading weather file.')

            df = pd.DataFrame(wx, index=dates)

            dates = []
            years = list(set(df.index.year))
            for year in years:
                for m in range(12):
                    month = [31,28,31,30,31,30,31,31,30,31,30,31]
                    adate = dt(year, m + 1, month[m])
                    dates.append(adate)

            mnmth_p, mnmth_t = self.mnmnthly(df)

            self.data = pd.DataFrame(np.array([mnmth_p, mnmth_t]).T,
                index=dates, columns=['precipitation', 'temp_avg'])

            
    def mnmnthly(self, df):
        years = list(set(df.index.year))

        mnmnthly_precip = []
        mnmnthly_temp = []

        y = -1
        for year in years:
            y += 1

            for m in range(12):
                start = dt(year, m+1, 1)
                rng = pd.date_range(start, start + MonthEnd(), freq='D')

                vals = df.loc[rng,'precip'].values
                # vals = np.nan_to_num(vals)
                mnmnthly_precip.append(np.mean(vals))

                vals = df.loc[rng,'air_temp_mean'].values
                # vals = np.nan_to_num(vals)
                mnmnthly_temp.append(np.mean(vals))

        return mnmnthly_precip, mnmnthly_temp


        