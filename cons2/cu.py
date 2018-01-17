# crop.py
# Derek Groenendyk
# 5/3/2016
# Crop classes for xcons program
"""


"""

from datetime import datetime as dt
from datetime import date
from itertools import islice
import logging
import numpy as np
import os
import pandas as pd
import pickle as pkl

logger_fn = logging.getLogger('crop_functions')
logger_fn.setLevel(logging.DEBUG)
logger_cu = logging.getLogger('crop_cu')


class CONSUMPTIVE_USE(object):
    """docstring for CONSUMPTIVE_USE"""
    def __init__(self, sp, cp):
        self.sp = sp
        self.cp = cp
        if self.sp.et_method == 'scs':
            self.ckc = self.cp.ckc
            self.nckc = self.cp.nckc

        if self.cp.crop_type == 'ANNUAL':
            self.mmnum = self.cp.mmnum
            self.ngrwpts = 21

        elif self.cp.crop_type == 'PERENNIAL':
            self.mmnum = 7
            self.ngrwpts = 25

        self.grow_dates = {}
            
        self.nyrs = len(self.sp.yrs)

        wx_years = list(set(self.sp.wx.data.index.year))
        # if (not np.all(wx_years == self.sp.yrs)) or \
        if (len(wx_years) < self.nyrs):
                logger_cu.warn('Missing years of weather data.')

        logger_cu.info('completed init: ' + self.cp.sname)

        
    def calc_temp(self):
        self.temps, self.days = self.mmtemp(self.nbegmo, 
                                       self.midpts, 
                                       self.npart, 
                                       self.mmnum)
        # might create an issues when they are equal, should probably
        # set tempf and dayf to zero. DGG 5/10/2016
        if self.nbegmo != self.nendmo: 
            self.tempf, self.dayf = self.mmtemp(self.nendmo, 
                                           self.midptf,
                                           self.nendda,
                                           12)

    def set_dates(self):
        if self.sp.et_method == 'scs':
            atemps = self.sp.wx.data['temp_avg']  
            self.get_dates(atemps)
        elif self.sp.et_method  == 'fao':
            self.beg = self.cp.beg
            self.end = self.cp.end            
            # self.beg = [self.jln(self.cp.mbegmo, self.cp.mbegda)] * len(self.sp.yrs)
            # self.end = [self.jln(self.cp.mendmo, self.cp.mendda)] * len(self.sp.yrs)


    def calc_dates(self):
        self.nbeg = self.beg[self.yr]
        self.nend = self.end[self.yr]

        # print(self.nbeg, self.nend, self.cp.sname)

        # if    self.nend - self.nbeg + 1 > self.cp.ngrows:
        #   self.nend = self.nbeg + self.cp.ngrows - 1

        dates = {}
        dates['nbegmo'], dates['nbegda'] = self.clndr(self.nbeg)
        dates['nendmo'], dates['nendda'] = self.clndr(self.nend)

        # print(dates,self.cp.sname)

        self.nbegmo = dates['nbegmo']
        self.nbegda = dates['nbegda']
        self.nendmo = dates['nendmo']
        self.nendda = dates['nendda']

        self.grow_dates[self.sp.yrs[self.yr]] = dates

        if self.nbeg > self.nend:
            logger_cu.warning('Beginning date is after ending' + \
                               'day for crop: ' + self.cp.sname)

        self.calc_midpts()

        if self.cp.crop_type == 'ANNUAL':
            # winter wheat
            if self.nbegmo == self.nendmo:
                self.midpts = ((self.nendda - self.nbegda + 1) / 2.) + self.nbegda

        elif self.cp.crop_type == 'PERENNIAL':
            # Julian spring midpoint of part month
            self.midspr = self.nbeg - self.nbegda + self.midpts
            self.midfal = self.nend - self.midptf


    def calc_kc(self):

        if self.cp.crop_type == 'ANNUAL':
            self.fake = self.nend - self.nbeg
            self.naccum[self.nbegmo-1] = self.jln(self.nbegmo, self.midpts) - self.nbeg
            self.nperct[self.nbegmo-1] = (self.naccum[self.nbegmo-1] / \
                                           self.fake) * 100.0
            self.midspr = self.nperct[self.nbegmo-1]
            self.midfal = self.nperct[self.nendmo-1]

        # Interpolate KC for part Spring month
        xkc, xf, xkt = self.interp_kc(self.midspr, self.temps, self.days)
        self.xkc[self.nbegmo - 1] = xkc
        self.xf[self.nbegmo - 1] = xf
        self.xkt[self.nbegmo - 1] = xkt

        # KC computation for all months
        if self.cp.crop_type == 'ANNUAL':
            # not winter wheat
            if self.nbegmo != self.nendmo:
                # not winter wheat
                if self.nbegmo != self.nendmo - 1:
                    self.kc_ann()

                self.naccum[self.nendmo-1] = self.nend - self.nbeg - \
                    (self.nendda + 1)/2.
                self.nperct[self.nendmo-1] = (self.naccum[self.nendmo-1] / \
                    self.fake) * 100.0

        elif self.cp.crop_type == 'PERENNIAL':
            self.kc_per()
       
        # Interpolate KC for part Fall month
        xkc, xf, xkt = self.interp_kc(self.midfal, self.tempf, self.dayf)
        self.xkc[self.nendmo - 1] = xkc
        self.xf[self.nendmo - 1] = xf
        self.xkt[self.nendmo - 1] = xkt


    def kc_ann(self):
        for k in range(self.nbegmo, self.nendmo-1):
            self.naccum[k] = self.jln(k+1, 15) - self.nbeg
            self.nperct[k] = (self.naccum[k] / self.fake) * 100.0
            flag = True
            for j in range(self.ngrwpts):
                if self.nckc[j] > self.nperct[k]:
                    self.xkc[k] = self.ckc[j-1] + (self.ckc[j] - \
                                  self.ckc[j-1]) * ((self.nperct[k] - \
                                  self.nckc[j-1]) / (self.nckc[j] - \
                                  self.nckc[j-1]))
                    flag = False
                    break                    
                elif self.nckc[j] == self.nperct[k]:
                    self.xkc[k] = self.ckc[j]
                    flag = False
                    break
            if flag:
                self.xkc[k] = self.ckc[j-1] + (self.ckc[j] - \
                              self.ckc[j-1]) * ((self.nperct[k] - \
                              self.nckc[j-1]) / (self.nckc[j] - \
                              self.nckc[j-1]))

            self.xf[k] = self.atemps[k] * self.sp.pclite[k] / 100.
            
            if self.atemps[k] < 36.0:
                self.xkt[k] = 0.3
            else:                    
                self.xkt[k] = 0.0173 * self.atemps[k] - 0.314


    def kc_per(self):
        mid = 15
        for k in range(self.nbegmo, self.nendmo-1):
            flag = True
            for j in range(self.ngrwpts):
                if self.nckc[j] == self.jln(k+1, mid):
                    self.xkc[k] = self.ckc[j]
                    flag = False
                    break
            if flag:
                logger_cu.warning('kc not found')

            self.xf[k] = self.atemps[k] * self.sp.pclite[k] \
            / 100.

            if self.atemps[k] < 36.0:
                self.xkt[k] = 0.3
            else:
                self.xkt[k] = 0.0173 * self.atemps[k] - 0.314


    def calc_cu(self):
        self.set_dates()
                
        self.pcu = np.zeros((self.nyrs, 13))
        self.pre = np.zeros((self.nyrs, 13))
        self.pcuirr = np.zeros((self.nyrs, 13))

        self.ppcu = np.zeros((self.nyrs, 13))
        self.ppre = np.zeros((self.nyrs, 13))
        self.pcuir = np.zeros((self.nyrs, 13))

        self.adjureq = np.zeros((self.nyrs))
        self.winprep = np.zeros((self.nyrs))        

        for yr in range(self.nyrs):
            self.yr = yr

            year = self.sp.wx.data.index.year
            self.atemps = self.sp.wx.data[year == \
                     self.sp.yrs[self.yr]].temp_avg.values

            precip = self.sp.wx.data[year == self.sp.yrs[yr]].precipitation.values   

            self.calc_dates()

            self.cu = np.zeros(13)
            self.nperct = np.zeros(12, dtype=np.int32)
            self.naccum = np.zeros(12, dtype=np.int32)            

            if self.sp.et_method == 'scs':
                self.calc_temp()
                self.xf = np.zeros(12)
                self.xkt = np.zeros(12)
                self.xkc = np.zeros(12)
                self.calc_kc()
                self.cu[:12] = self.xf * self.xkt * self.xkc

            elif self.sp.et_method == 'fao':
                self.cu[:12] = self.calc_fao(yr)


            re, cuirr = self.calc_effprecip(precip)

            self.ppcu[yr] = self.cu
            self.ppre[yr] = re
            self.pcuir[yr] = cuirr

        logger_cu.info('finished cu calculation')


    def spring(self, atemp, mean):
        """
        Find beginning of growing season day of year.

        Parameters
        ----------
        atemp: float
            Temperature
        mean: float
            Critical spring growing season temperature

        Returns
        -------
        jdays: integer
            Julian day
        """

        if atemp[6] >= mean:
            for j in range(0, 7):
                i = 6 - j
                if atemp[i] <= mean:
                    break
            try:
                idiff = 30 * (mean - atemp[i]) / (atemp[i+1] - atemp[i])
            except ZeroDivisionError:
                idiff = 0
            if idiff > 15 and idiff < 31:
                month = i + 2
                kdays = idiff - 15
            elif idiff <= 15 and idiff > 0:
                month = i + 1
                kdays = idiff + 15
            elif idiff >= 31:
                month = i + 2
                kdays = 15
            elif idiff <= 0:
                month = i + 1    
                kdays = 15
        else:
            month = 7
            kdays = 15

        kdays = int(round(kdays))

        # try:
        #     kdays = int(round(kdays))
        # except OverflowError:
        #     logger_fn.critical('Invalid kdays value')
        #     logger_fn.critical('', mean, atemp[i], atemp[i]+1)
        #     raise

        if kdays < 1:
            kdays = 1
        if month == 2 and kdays > 28:
            kdays = 28

        # yday = d.toordinal() - date(d.year, 1, 1).toordinal() + 1
        jdays = dt(2015, int(month), round(kdays)).timetuple().tm_yday

        return jdays


    def fall(self, atemp, mean):
        """
        Find end of growing season day of year.

        Parameters
        ----------
        atemp: float
            Temperature
        mean: float
            Critical spring growing season temperature

        Returns
        -------
        jdays: integer
            Julian day
        """

        flag = True
        for i in range(6, 11):
            if atemp[i + 1] < mean:
                try:
                    idiff = 30 * (atemp[i] - mean) / (atemp[i] - atemp[i+1])
                except ZeroDivisionError:
                    idiff = 0
                if idiff > 15 and idiff < 31:
                    month = i + 2
                    kdays = idiff - 15
                elif idiff <= 15 and idiff > 0:
                    month = i + 1
                    kdays = idiff + 15
                elif idiff >= 31:
                    month = i + 2
                    kdays = 15
                elif idiff <= 0:
                    month = i + 1    
                    kdays = 15
                flag = False
                break
        if flag:
            month = 12
            kdays = 15

        kdays = int(round(kdays))

        if kdays < 1:
            kdays = 1
        if month == 2 and kdays > 28:
            kdays = 28
        jdays = dt(2015, month, kdays).timetuple().tm_yday

        return jdays


    def clndr(self, doy):
        """
        Convert day of year in month and day.

        Parameters
        ----------
        doy: integer
            Julian day of the year

        Returns
        -------
        month: integer
            Month of the year
        day: integer
            Day of the month
        """

        ordinal = date.toordinal(date(2015, 1, 1)) + int(doy) - 1
        adate = date.fromordinal(ordinal).timetuple()
        month = int(adate[1])
        day = int(adate[2])

        return month, day


    def jln(self, m, d):
        return dt(2015, m, d).timetuple().tm_yday


    def get_dates(self, temps):
        """
        Find the start and end of the 
        crop growth season in julian days

        Parameters
        ----------
        temps: float
            Monthly mean Spring temperature
        years: list
            List of integer years
        nbtemp: float
            Temperature when the growing season begins
        netemp: float
            Temperature when the growing season ends
        mbegmo: integer
            Earliest month season can begin
        mbegda: integer
            Earliest day season can begin
        mendmo: integer
            Latest month season can end
        mendda: integer
            Latest day season can end

        Returns
        -------
        nbeg: integer
            Julian day
        nend: integer
            Julian day
        """
        nyrs = len(self.sp.yrs)

        self.beg = np.zeros((nyrs), dtype=np.int32)
        self.end = np.zeros((nyrs), dtype=np.int32)

        # mbeg = self.jln(self.cp.mbegmo, self.cp.mbegda)
        # mend = self.jln(self.cp.mendmo, self.cp.mendda)

        for yr in range(nyrs):
            mbeg = self.jln(self.cp.mbegmo[yr], self.cp.mbegda[yr])
            mend = self.jln(self.cp.mendmo[yr], self.cp.mendda[yr])
            if mend <= mbeg:
                # print(mbeg, mend)
                mbeg = mbeg - mend + 1
                mend = 365 - mend + 1

            atemp = temps[temps.index.year == self.sp.yrs[yr]].values
            if self.sp.units == 'metric':
                atemp = atemp * 1.8 + 32.

            nstart = self.spring(atemp, self.cp.nbtemp)
            self.beg[yr] = nstart
            # winter wheat spring
            if (nstart - mbeg) <= 0.:
                self.beg[yr] = mbeg

            mend = self.beg[yr] + self.cp.ngrows
            # if 'wheat' in self.cp.sname:
                # print(mend)
            if mend > 365:
                if self.beg[yr] > (mend - 365) - 1:
                    self.beg[yr] -= (mend - 365) - 1
                    mend = 365 - (mend - 365)
                else:
                    mend = 365

            kend = self.fall(atemp, self.cp.netemp)                
            self.end[yr] = kend
            # winter wheat fall
            if (kend - mend) >= 0.:
                self.end[yr] = mend
                # self.end[yr] = self.beg[yr] + self.cp.ngrows

            # if 'wheat' in self.cp.sname.lower():\
                # print(self.beg[yr], self.end[yr], mbeg, mend, kend)

            if self.beg[yr] > self.end[yr]:
                logger_fn.critical('beginning date is after ending date for crop ' + self.cp.sname)
                raise


    def calc_midpts(self):
        """
        Find midpoints of seasons

        Parameters
        ----------
        nbegmo: integer
            Month growing season begins
        nbegda: integer
            Day of the month for the beginning of the growing season
        nendda: 
            Day of the month for the end of the growing season

        Returns
        -------
        npart: integer
            First part of first month of the season
        midpts: integer
            Midpoint of the Spring month of the season
        midptf: integer
            Midpoint of the Fall month of the season
        """

        month = [31,28,31,30,31,30,31,31,30,31,30,31]
        self.npart = month[self.nbegmo-1] - self.nbegda + 1
        self.midpts = int(self.npart / 2. + self.nbegda)
        self.midptf = int((self.nendda + 1) / 2.)


    def mmtemp(self, nmo, midpt, day2, num):
        """
        Caclulates Spring part month mean temperature

        Parameters
        ----------
        nmo: integer
            Month number
        midpt: integer
            Midpoint day of the month
        day2: integer
            Day of  month
        num: integer
            Number of months to use
        atemps: list
            List of temperatures for the year
        pclite: list
            List of fraction light for each month
        middle: list
            Middle day for each month

        Returns
        -------
        temp: float
            Mean montly temperature
        day: integer
            Day of the month
        """ 
        middle = [16, 45, 75, 105, 136, 166, 197, 228, 258, 289, 319, 350]

        for k in range(num):
            # logger_fn.info(str(self.jln(nmo, midpt)) + ', ' + str(middle[k]))
            if self.jln(nmo, midpt) < middle[k]:
                temp = self.midtemp(nmo, midpt, k, self.atemps, middle)
                day = self.midday(nmo, midpt, day2, k, self.sp.pclite, middle)
                return temp, day
            elif self.jln(nmo, midpt) == middle[k]:
                temp = self.atemps[k] 
                day = self.sp.pclite[k]
                return temp, day
        logger_fn.warn("mean monthly temperature not found, month can't be found.")
        

    def midtemp(self, nmo, midpt, k, temp, middle):
        """
        Calculates mean monthly temperature

        Parameters
        ----------

        """
        day1 = self.jln(nmo, midpt)
        return temp[k-1] + ((day1 - middle[k-1]) / (middle[k] - \
               middle[k-1])) * (temp[k] - temp[k-1])


    def midday(self, nmo, midpt, day2, k, pclite, middle):
        month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day1 = self.jln(nmo, midpt)
        return (pclite[k-1] + ((day1 - middle[k-1]) / (middle[k] \
               - middle[k-1])) * (pclite[k] - pclite[k-1])) * (day2 / month[nmo-1])


    def interp_kc(self, mid, temp, day):
        flag = True
        for k in range(self.ngrwpts):
            if self.nckc[k] > mid:
                xkc = self.ckc[k-1] + (self.ckc[k] - self.ckc[k-1]) * ((mid - self.nckc[k-1]) \
                    / (self.nckc[k] - self.nckc[k-1]))
                flag = False
                break
            elif self.nckc[k] == mid:
                xkc= self.ckc[k]
                flag = False
                break
        if flag:
            xkc = self.ckc[k-1] + (self.ckc[k] - self.ckc[k-1]) * ((mid - self.nckc[k-1]) \
                / (self.nckc[k] - self.nckc[k-1]))
        xf = temp * day / 100.

        if temp < 36.:
            xkt = 0.3
        else:
            xkt = 0.0173 * temp - 0.314
                
        return xkc, xf, xkt


    def calc_effprecip(self, precip):

        if self.sp.units == 'metric':
            precip /= 25.4

        month = [31,28,31,30,31,30,31,31,30,31,30,31]

        if self.sp.apdep == 0.:
            f = 1.0
        elif self.sp.apdep > 0.:
            f = 0.531747 + 0.295164 * self.sp.apdep - 0.057697 * self.sp.apdep**2 + 0.003804 * \
                self.sp.apdep**3

        re = np.zeros((13))
        cuirr = np.zeros((13))
        
        for k in range(12):
            # if units == 'metric':
                # cu_temp = cu[k] / 25.4
            # else:
            cu_temp = self.cu[k]
            if self.sp.npre != 2:
                # verify this calculation - DGG 2/13/2017
                if k == self.nbegmo-1:
                    cu_temp *= month[self.nbegmo-1] / self.npart
                if k == self.nendmo-1:
                    cu_temp *= month[self.nendmo-1] / self.nendda
                
                re[k] = (0.70917 * precip[k]**0.82416 - 0.11556) * f * \
                        10**(0.02426 * cu_temp)

                if k == self.nbegmo-1:
                    cu_temp *= self.npart / month[self.nbegmo-1]
                if k == self.nendmo-1:
                    cu_temp *= self.nendda / month[self.nendmo-1]
            else:
                if precip[k] <= 1.0:
                    re[k] = precip[k] * 0.95
                elif precip[k] <= 2.0:
                    re[k] = ((precip[k] - 1.0) * 0.9) + 0.95
                elif precip[k] <= 3.0:
                    re[k] = ((precip[k] - 2.0) * 0.82) + 1.85
                elif precip[k] <= 4.0:
                    re[k] = ((precip[k] - 3.0) * 0.65) + 2.67
                elif precip[k] <= 5.0:
                    re[k] = ((precip[k] - 4.0) * 0.45) + 3.32
                elif precip[k] <= 6.0:
                    re[k] = ((precip[k] - 1.0) * 0.05) + 4.02

            if re[k] < 0.0:
                re[k] = 0.0
            if re[k] > precip[k]:
                re[k] = precip[k]

            x = month[k]

            if k == self.nbegmo-1:
                re[k] = ((x - self.nbegda + 1.0) / x) * re[k]
            if k == self.nendmo-1:
                re[k] = (self.nendda / x) * re[k]
            # winter wheat, double check DGG 4/3/2017
            if self.nbegmo-1 == k and self.nendmo-1 == k:
                re[k] = ((self.nendda - self.nbegmo + 1) / x) *re[k]
            if re[k] > cu_temp:
                re[k] = cu_temp
            cuirr[k] = cu_temp - re[k]

            self.cu[12] += cu_temp
            re[12] += re[k]
            cuirr[12] += cuirr[k]

        return re, cuirr


    def calc_adj(self, cuirr, pccrop, precip, nbegmo, day3):
        month = [31,28,31,30,31,30,31,31,30,31,30,31]
        smosadj = 0.0
        for i in range(nbegmo - 1):
            smosadj += precip[i]
        smosadj += precip[nbegmo] * (month[nbegmo-1] - day3) / month[nbegmo - 1]
        if smosadj > 3.0:
            smosadj = 3.0
        if (cuirr[-1] - smosadj) < 0.0:
            smosadj = cuirr[-1]
        adjureq = (cuirr[-1] - smosadj) * pccrop / 100.0
        # winprep = smosadj * precip / 100.0 # why? what is the purpose?
        winprep = 0.0

        return adjureq, winprep


    def fiveyr_avg(self, yr, fivc, fivcr, pcu, pcuirr):
        fivcu = fivc[yr-4] + fivc[yr-3] + fivc[yr-2] + fivc[yr-1] + fivc[yr]
        fivci = fivcr[yr-4] + fivcr[yr-3] + fivcr[yr-2] + fivcr[yr-1] + fivcr[yr]
        fvcup = pcu[yr-4, -1] + pcu[yr-3, -1] + pcu[yr-2, -1] + pcu[yr-1, -1] + \
                pcu[yr, -1]
        fvcip = pcuirr[yr - 4, -1] + pcuirr[yr - 3, -1] + pcuirr[yr - 2, -1] + \
                pcuirr[yr - 1, -1] + pcuirr[yr, -1]

        return fivc, fivci, fvcup, fvcip


    def calc_fao(self, yr, repeat=1):

        lfrac = self.cp.stages[self.cp.stype]
        kc_vals = self.cp.kc[self.cp.kcnum]

        start_date = dt(self.sp.yrs[yr], self.nbegmo, self.nbegda)

        ETo = np.zeros((12))
        Kc = np.zeros((12))

        pclite = self.calc_pclite(self.sp.latitude)

        for k in range(repeat):
            date_rng = pd.date_range(start_date, periods=self.cp.ngrows, freq='D')

            months = sorted(list(set(date_rng.month)))

            total_days = 1.0

            for i in range(len(months)):

                num_modays = len(np.nonzero(date_rng.month == months[i])[0])

                ind = str(self.sp.yrs[yr]) + '-' + str(months[i])

                kc_total = 0
                for aday in range(num_modays):
                    nday = total_days + float(aday)
                    kc_total += self.calc_faokc(nday/float(self.cp.ngrows), lfrac, kc_vals)

                temp_Kc = kc_total/num_modays
                            
                p = pclite[months[i]-1]

                temp_ETo = self.fao_cu(p, self.atemps[months[i]-1])
                temp_ETo *= num_modays

                total_days += num_modays            

                ETo[months[i]-1] += temp_ETo
                if Kc[months[i]-1] != 0.:
                    Kc[months[i]-1] = (Kc[months[i]-1] + temp_Kc)/2
                else:
                    Kc[months[i]-1] = temp_Kc

            start_date = date_rng[-1]+1

        ETc = ETo*Kc/25.4

        return ETc


    def calc_pclite(self, lat):

        pclite_dict = {}
        pclite_dict[30] = np.array([.24, .25, .27, .29, .31, .32, .31, .30, .28, .26, .24, .23])
        pclite_dict[35] = np.array([.23, .25, .27, .29, .31, .32, .32, .30, .28, .25, .23, .22])
        
        if lat > 35 or lat < 30:
            logger_fn.critical("Latitude out of bounds for pclite. 30* <= lat <= 35* ")
            raise

        if lat in pclite_dict.keys():
            return pclite_dict[lat]
        else:
            dx = (35. - lat)/(35.-30.)
            return pclite_dict[35] + dx*(pclite_dict[30] - pclite_dict[35])


    def fao_cu(self, p, tavg):
        f = p * (0.46 * tavg + 8.13)

        # low humidity, high n/N, medium wind
        # a = -2.30
        # b = 1.82
        # low humidity, high n/N, low wind    
        a = -2.60
        b = 1.55

        ETO = a + b * f

        return ETO


    def calc_faokc(self, frac, lfrac, kc):

        if frac < lfrac[0]:
            kc_aday = kc[0]

        elif frac < np.sum(lfrac[:2]):
            dx = np.sum(lfrac[:2]) - lfrac[0]
            kc_aday = ((frac-lfrac[0]))*((kc[1] - kc[0])/dx) + kc[0]

        elif frac < np.sum(lfrac[:3]):
            kc_aday = kc[1]

        elif frac <= np.sum(lfrac):
            dx = np.sum(lfrac) - np.sum(lfrac[:3])
            kc_aday = kc[1] - (frac-np.sum(lfrac[:3]))*((kc[1] - kc[2])/dx)
        else: # accounts for inaccuracy in np.sum(), essentially kc_aday = kc[2]
            dx = np.sum(lfrac) - np.sum(lfrac[:3])
            kc_aday = kc[1] - (frac-np.sum(lfrac[:3]))*((kc[1] - kc[2])/dx)

        return kc_aday
