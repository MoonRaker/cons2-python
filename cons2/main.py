# cons2.py
# Derek Groenendyk
# 5/3/2016
# Rewritten from a USDA XCONS program that uses Blaney-Criddle method for
# calculating consumptive use.


# '''
# This program was translated into Python from a Fortran program written
# by USDA in 1980. 

# "PROGRAM XCONS

# COMPUTES CONSUMPTIVE USE AS PRESENTED IN SCS TECHNICAL RELEASE NO. 21
# -- REVISED SEPTEMBER 1970.

# THE PROGRAM WAS ORIGINALLY DEVELOPED BY JOE WENSMAN OF THE PN REGIONAL
# OFFICE AS PROGRAM CONSUSE.

# THIS PROGRAM WAS ACQUIRED BY D-752 IN JANUARY, 1981 AND MODIFIED SLIGHTLY.
# THESE MODIFICATIONS ALLOW FOR OUTPUT OF SUMMARY TABLES ONLY AND
# ELIMINATION OF THE SEASON BY SEASON SUMMARIES, USE OF DEPTHS OTHER
# THAN THREE INCHES FOR COMPUTATION OF EFFECTIVE PRECIPITATION, USE
# OF UP TO 100 YEARS OF DATA IN THE COMPUTATIONS (AS OPPOSED TO THE
# ORIGINAL 60 YEAR LIMIT) AND PRINTING OF YEARS BETWEEN 1900 AND 1909.
     
# +------------------------+-----------------------+
# | Crop Number            | Crop Name             |
# +========================+=======================+
# | 1                      | ALFALFA               |
# +------------------------+-----------------------+
# | 2                      | GRASS PASTURE         |
# +------------------------+-----------------------+
# | 3                      | ORCHARD WITHOUT COVER |
# +------------------------+-----------------------+
# | 4                      | ORCHARD WITH COVER    |
# +------------------------+-----------------------+
# | 5*                     | CITRUS                |
# +------------------------+-----------------------+
# | 6                      | GRAPES                |
# +------------------------+-----------------------+
# | 7                      | DRY BEANS             |
# +------------------------+-----------------------+
# | 8                      | SPRING GRAIN          |
# +------------------------+-----------------------+
# | 9                      | CORN SILAGE           |
# +------------------------+-----------------------+
# | 10*                    | COTTON 1              |
# +------------------------+-----------------------+
# | 11                     | IRISH POTATOES        |
# +------------------------+-----------------------+
# | 12                     | SMALL VEGETABLES      |
# +------------------------+-----------------------+
# | 13                     | CORN SWEET            |
# +------------------------+-----------------------+
# | 14                     | SNAP BEANS            |
# +------------------------+-----------------------+
# | 15                     | CORN GRAIN            |
# +------------------------+-----------------------+
# | 16                     | DRY PEAS              |
# +------------------------+-----------------------+
# | 17                     | GREEN PEAS            |
# +------------------------+-----------------------+
# | 18                     | COTTON 2              |
# +------------------------+-----------------------+
# | 19                     | WINTER WHEAT FALL     |
# +------------------------+-----------------------+
# | 20                     | WINTER WHEAT SPRING   |
# +------------------------+-----------------------+

# *CROPS 10 AND 5 HAVE BEEN MODIFIED FOR USE IN AZ

# CROPS 1-6 ARE PERENNIAL CROPS WITH CROP GROWTH STAGE COEFFICIENT CURVE VALUES
# ON THE 1ST AND 15TH OF EACH MONTH (25 points)

# CROPS 7-20 ARE ANNUAL CROPS WITH CROP GROWTH STAGE COEFFICIENT CURVE VALUES
# AT 5 PERCENT OF GROWING SEASON INTERVALS;

# CROP GROWTH STAGE COEFFICIENT CURVE VALUES TAKEN FROM SCS TECH. REL. NO. 21,
# 1970, UNLESS (EST)"
    
# '''

from datetime import datetime as dt
from datetime import date
import logging
import numpy as np
import os
import pandas as pd
import sys

import cons2

# from cons2.crop import ALFALFA, GRPASTURE, ORCHARDCOVER, ORCHARDNOCOVER, CITRUS, \
#                  GRAPES, DRYBEANS, SPRGRAIN, CORNSILAGE, COTTON1, \
#                  IRPOTATOES, SMVEGETABLES, SWEETCORN, SNAPBEANS, \
#                  CORNGRAIN, DRYPEAS, GREENPEAS, COTTON2, WNTRWHEATFALL, \
#                  WNTRWHEATSPRING

from cons2.site import SITE
# from cons2.crop import CROP
# from cons2.read_infile import get_data
import cons2.excel as excel
# from cons2.weather import WEATHER


# crp_classes = [ALFALFA, GRPASTURE, ORCHARDCOVER, ORCHARDNOCOVER, CITRUS, \
#                  GRAPES, DRYBEANS, SPRGRAIN, CORNSILAGE, COTTON1, \
#                  IRPOTATOES, SMVEGETABLES, SWEETCORN, SNAPBEANS, \
#                  CORNGRAIN, DRYPEAS, GREENPEAS, COTTON2, WNTRWHEATFALL, \
#                  WNTRWHEATSPRING]          

# logging.basicConfig(filename='cons2.log', 
#                     level=logging.DEBUG,
#                     # level=logging.INFO,
#                     # level=logging.CRITICAL,
#                     # level=logging.WARNING,
#                     format='%(asctime)s %(name)-15s %(levelname)-8s %(message)s',
#                     datefmt='%m-%d %H:%M',
#                     filemode='w')
# logger = logging.getLogger('cons2_main')

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

cons2_dir = os.path.dirname(os.path.abspath(cons2.__file__))

# ch = logging.StreamHandler(sys.stdout)
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)


def import_data(vis):
    """
    Reads the site input file and initilizes a SITE object, including crop
    and weather information.

    Parameters
    ----------
    vis: boolean
        Sets Excel object visibility.

    Returns
    -------
    sites: list
        SITE objects for each input location.
    """

    directory = os.getcwd()
    dir_list = os.listdir(directory)

    # test_dir = os.path.dirname(os.path.abspath(
    #          inspect.getfile(inspect.currentframe())))
    # file = os.path.join(test_dir, '..', 'data', 'detect_clearsky_data.csv')
    
    # cons2_dir = os.path.dirname(os.path.abspath(cons2.main.__file__))

    # cwb = ex.open_workbook(os.path.join(cons2_dir,'data','crop_parameters.xlsx'), vis)

    # if cwb == None:
    #     logger.critical('Please close workbook: ' + 'crop_parameters.xlsx')
    #     raise SystemExit    

    # file_list = []
    # for afile in dir_list:
    #     if 'sites_in.xlsx' in afile and '~' not in afile:
    #         file_list.append(afile)

    sites = []
    if 'sites_in.xlsx' in dir_list:
        # for afile in file_list:
        # swb = ex.open_workbook(os.path.join(directory, 'sites_in.xlsx'), vis)
        # print(os.path.join(directory, 'sites_in.xlsx'))
        sin_ex = excel.Excel(os.path.join(directory, 'sites_in.xlsx'), vis)
        swb = sin_ex.wb
        # if swb == None:
        #     logger.critical('Please close workbook: ' + 'sites_in.xlsx')
        #     raise SystemExit
        sheets = list(swb.Worksheets)
        for sheet in swb.Worksheets:
            # asite = SITE(directory + '\\' + afile)
            # print(sheets[i].Name)

            asite = SITE(sheet)

            # asite.wx = WEATHER(asite.wx_file, asite.wx_location, units='english')
                
            if isinstance(asite.wx.data, pd.DataFrame):
                sites.append(asite)                  

            logger.info('finished initializing site: ' \
                + asite.site_name)
        # swb.Close(1)
        sin_ex.close_workbook(0)
    else:
        logger.critical('sites_in.xlsx file not present.')
        # cwb.Close(0)
        # ex.close()
        # cp_ex.close_workbook(0)
        raise SystemExit   

    # cwb.Close(0)
    # cp_ex.close_workbook(0)

    return sites


def write_output(directory, name, years, data):
    """
    Writes summary data for consumptive use, effective precipitation,
    and irrigrated consumptive for the whole site.

    Parameters
    ----------
    directory: string
        Directory where .csv files will be saved.
    name: string
        Name of the site.
    years: list
        List of integer years for the site.
    data: list
        List of arrays containing the data for each variable.
    """

    var_names = ['pcu', 'pre', 'pcuir', 'totals']

    headers = ['','Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.',
        'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']

    for i in range(len(data)):
        outfile = open(os.path.join(directory,'_'.join([var_names[i],
            name + '.csv'])), 'w')
        outlines = [','.join(headers) + '\n']
        for yr in range(data[i].shape[0]):
            pdata = [str(round(item, 2)) for item in data[i][yr]]
            outlines.append(','.join([str(years[yr]), *pdata, '\n']))

        pdata = [str(round(item, 2)) for item in np.mean(data[i], axis=0)]

        outlines.append(','.join(['average', *pdata, '\n']))

        outfile.writelines(outlines)
        outfile.close()

    headers = ['', 'cu', 're', 'cuirr']

    outfile = open(os.path.join(directory,'_'.join([var_names[-1],
        name + '.csv'])), 'w')
    outlines = [','.join(headers) + '\n']

    for i in range(len(years)):
        pdata = [str(data[0][i, -1]), str(data[1][i, -1]), str(data[2][i, -1])]
        outlines.append(','.join([str(years[i]), *pdata, '\n']))
        
    pdata = [
        str(round(np.mean(data[0][:, -1]), 2)),
        str(round(np.mean(data[1][:, -1]), 2)),
        str(round(np.mean(data[2][:, -1]), 2))
    ]
    outlines.append(','.join(['average', *pdata, '\n\n']))


    outfile.writelines(outlines)
    outfile.close()

    logger.info('finished writing site wide output files for: ' + name)


def write_crp_output(directory, name, cname, years, data, dates, starts, 
                     ends, bwrite):
    """
    Writes output data for each crop.

    Parameters
    ----------
    directory: string
        Directory where .csv files will be saved.
    name: string
        Name of the site.
    cname:
        Name of the crop.
    years: list
        List of integer years for the site.
    data: list
        List of arrays containing the data for each variable.
    dates: list
        Planting season dates.
    starts: list
        List of Julian dates for the begining of the growing season.
    ends: list
        List of Julian dates for the end of the gowring season.
    bwrite: boolean
        Logical determing whether or not to print individual crop files.
    """

    var_names = ['cu', 're', 'cuirr', 'totals']

    headers = ['','Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.',
        'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']

    # write output file for each crop variable
    if bwrite:
        for i in range(len(data)):
            outfile = open(os.path.join(directory,'_'.join([var_names[i], 
                           name, cname + '.csv'])), 'w')
            # outfile = open(name + '_' + cname + '_' + var_names[i] + '.csv', 'w')
            outlines = [','.join(headers) + '\n']
            for yr in range(data[i].shape[0]):
                pdata = [str(round(item, 2)) for item in data[i][yr]]
                outlines.append(','.join([str(years[yr]), *pdata, '\n']))

            pdata = [str(round(item, 2)) for item in np.mean(data[i], axis=0)]

            outlines.append(','.join(['average', *pdata, '\n\n']))

            outlines.append(','.join(['growing season', 'start', 'end',
                                     'length', '\n']))
            for yr in range(len(years)):
                temp_dates = [
                    '{}/{}'.format(dates[years[yr]]['nbegmo'], 
                        dates[years[yr]]['nbegda']),
                    '{}/{}'.format(dates[years[yr]]['nendmo'],
                        dates[years[yr]]['nendda']),
                    '{}'.format(ends[yr]-starts[yr]+1),
                ]
                outlines.append(','.join([str(years[yr]), *temp_dates, '\n']))

            outfile.writelines(outlines)
            outfile.close()

    # write output file for the totals for each variable. 
    headers = ['', 'cu', 're', 'cuirr']

    outfile = open(os.path.join(directory,'_'.join([var_names[-1], name,
                   cname + '.csv'])), 'w')
    outlines = [','.join(headers) + '\n']

    for i in range(len(years)):
        pdata = [
            str(data[0][i, -1]),
            str(data[1][i, -1]), 
            str(data[2][i, -1])
        ]
        outlines.append(','.join([str(years[i]), *pdata, '\n']))
        
    pdata = [
        str(round(np.mean(data[0][:, -1]), 2)),
        str(round(np.mean(data[1][:, -1]), 2)),
        str(round(np.mean(data[2][:, -1]), 2))
    ]
    outlines.append(','.join(['average', *pdata, '\n']))

    outfile.writelines(outlines)
    outfile.close()

    logger.info('finished writing ' + cname + ' output files for : ' + name)


def write_excel_monthly(wb, name, etmethod, acrop, years, data, dates, starts, 
        ends):
    var_names = ['CU', 'Eff. P', 'Net CU', 'Totals']

    headers = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.',
        'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.', 'Total']

    cname = acrop.nickname
    cname = cname[0].upper() + cname[1:]

    sheets = wb.Worksheets
    try:
        ws = sheets(cname)
    except:
        ws = sheets.Add()
        ws.Name = cname
    ws.Cells(1, 1).Value = cname
    ws.Cells(1, 1).Font.Bold = True

    if etmethod == 'fao':
        ws.Cells(1, 2).Value = 'Season Type'
        ws.Cells(1, 2).Font.Bold = True
        ws.Cells(1, 3).Value = acrop.stype
        ws.Cells(1, 4).Value = 'Kc Num'
        ws.Cells(1, 4).Font.Bold = True
        ws.Cells(1, 5).Value = acrop.kcnum   

    rind = 2
    ws.Cells(rind, 1).Value = 'Growing Season'
    ws.Cells(rind, 2).Value = 'Start'
    ws.Cells(rind, 3).Value = 'End'
    ws.Cells(rind, 4).Value = 'Length'
    ws.Range(ws.Cells(rind, 1), ws.Cells(rind, 4)).Font.Bold = True

    tind = rind + 1
    for yr in range(len(years)):
        rind += 1
        temp_dates = [
            '{}/{}'.format(dates[years[yr]]['nbegmo'], 
                dates[years[yr]]['nbegda']),
            '{}/{}'.format(dates[years[yr]]['nendmo'],
                dates[years[yr]]['nendda']),
            '{}'.format(ends[yr]-starts[yr]+1),
        ]
        ws.Cells(rind, 1).Value = str(years[yr])
        ws.Cells(rind, 2).Value = temp_dates[0]
        ws.Cells(rind, 2).NumberFormat = "MM/dd"
        ws.Cells(rind, 3).Value = temp_dates[1]
        ws.Cells(rind, 3).NumberFormat = "MM/dd"
        ws.Cells(rind, 4).Value = temp_dates[2]
    ws.Range(ws.Cells(tind, 1), ws.Cells(rind, 1)).Font.Bold = True   

    # rind += 1
    # write output file for each crop variable
    for i in range(len(data)):
        rind += 2
        ws.Cells(rind, 1).Value = var_names[i]
        for j in range(len(headers)):
            ws.Cells(rind, j+2).Value = headers[j]
            ws.Cells(rind, j+2).Font.Bold = True
        ws.Range(ws.Cells(rind, 1), ws.Cells(rind, len(headers) + 1)).Font.Bold = True   

        tind = rind + 1
        for yr in range(data[i].shape[0]):
            rind += 1
            pdata = [str(round(item, 2)) for item in data[i][yr]]
            # if etmethod == 'bc':
            pdata = [str(round(item/12.0, 2)) for item in data[i][yr]]
            ws.Cells(rind, 1).Value = str(years[yr])
            for j in range(len(pdata)):
                ws.Cells(rind, j+2).Value = pdata[j]
        ws.Range(ws.Cells(tind, 1), ws.Cells(rind, 1)).Font.Bold = True   

        rind += 1
        pdata = [str(round(item, 2)) for item in np.mean(data[i], axis=0)]
        # if etmethod == 'bc':
        pdata = [str(round(item/12.0, 2)) for item in np.mean(data[i], axis=0)]        
        ws.Cells(rind, 1).Value = 'Average'
        ws.Cells(rind, 1).Font.Bold = True
        for j in range(len(pdata)):
            ws.Cells(rind, j+2).Value = pdata[j]
    ws.Columns.AutoFit()

def write_excel_yearly(wb, name, etmethod, acrop, years, data, dates, starts, 
        ends, rind):

    cname = acrop.nickname
    cname = cname[0].upper() + cname[1:]

    sheets = wb.Worksheets
    try:
        ws = sheets(name)
    except:
        ws = sheets.Add()
        ws.Name = name

    # write output file for the totals for each variable. 
    # headers = ['CU', 'Eff. P.', 'Net CU']
    # units = [' (in.)', ' (ft.)']

    rind += 1
    ws.Cells(rind, 1).Value = cname
    ws.Cells(rind, 1).Font.Bold = True
    if etmethod == 'fao':
        ws.Cells(rind, 2).Value = 'Season Type'
        ws.Cells(rind, 2).Font.Bold = True
        ws.Cells(rind, 3).Value = acrop.stype
        ws.Cells(rind, 4).Value = 'Kc Num'
        ws.Cells(rind, 4).Font.Bold = True
        ws.Cells(rind, 5).Value = acrop.kcnum    
 
    tind = rind + 1
    for i in range(len(years)):
        rind += 1
        ws.Cells(rind, 1).Value = str(years[i])
        ws.Cells(rind, 1).Font.Bold = True
        pdata = [
            str(round(data[0][i, -1], 2)),
            str(round(data[1][i, -1], 2)), 
            str(round(data[2][i, -1], 2))
            ]

        for j in range(3):
            ws.Cells(rind, 2+j).Value = pdata[j]
            ws.Cells(rind, 5+j).Value = round(float(pdata[j])/12.0, 2) 
                       
        # if etmethod == 'bc':
        #     for j in range(3):
        #         ws.Cells(rind, 2+j).Value = pdata[j]
        #     for j in range(3):
        #         ws.Cells(rind, 5+j).Value = round(float(pdata[j])/12.0, 2)
        # elif etmethod == 'fao':
        #     for j in range(3):
        #         ws.Cells(rind, 2+j).Value = round(float(pdata[j])*12.0, 2)
        #     for j in range(3):
        #         ws.Cells(rind, 5+j).Value = pdata[j]                 

    rind += 1
    pdata = [
        str(round(np.mean(data[0][:, -1]), 2)),
        str(round(np.mean(data[1][:, -1]), 2)),
        str(round(np.mean(data[2][:, -1]), 2))
        ]
    ws.Range(ws.Cells(tind, 1), ws.Cells(rind+1, 1)).Font.Bold = True  

    ws.Cells(rind, 1).Value = 'Average'
    for j in range(3):
        ws.Cells(rind, 2+j).Value = pdata[j]
        ws.Cells(rind, 5+j).Value = round(float(pdata[j])/12.0, 2)    
    # if etmethod == 'bc':
    #     for j in range(3):
    #         ws.Cells(rind, 2+j).Value = pdata[j]
    #     for j in range(3):
    #         ws.Cells(rind, 5+j).Value = round(float(pdata[j])/12.0, 2)
    # elif etmethod == 'fao':
    #     for j in range(3):
    #         ws.Cells(rind, 2+j).Value = round(float(pdata[j])*12.0, 2)   
    #     for j in range(3):
    #         ws.Cells(rind, 5+j).Value = pdata[j]         

    ws.Columns.AutoFit()

    logger.info('finished writing output files for : ' + name + ', ' + cname)


def run():
    """
    Runs the CONS2 program.
    """

    vis = False

    # crops = import_crops()

    # ex = excel.Excel(vis)

    # ex.setVis(False)

    # crops = [ALFALFA]
    # sparms, cparms = get_data('noga.i')
    # print(len(crp_classes))

    directory = os.getcwd()

    try:
        sites = import_data(vis)
    except Exception as err:
        logger.exception('Error Occurred')
        logger.critical('traceback:' + str(err))
        raise

    logger.info('initialized sites')

    # print(len(sites))
    # print(sites[0])

    # creates results directory
    results_dir = os.path.join(directory, 'results')
    if not os.path.exists(results_dir):
        os.mkdir(os.path.join(directory, 'results'))

    # wb_yearly = None
    # siteout_path = os.path.join(results_dir, 'sites_out.xlsx')

    # if os.path.exists(siteout_path):
    #     wb_yearly = ex.open_workbook(siteout_path, vis)
    #     if wb_yearly == None:
    #         logger.critical('Close workbook: '+'sites_out.xlsx')
    #         raise SystemExit
    #     else:
    #         wb_yearly.Close(0)
    #     os.remove(siteout_path)
    # wb_yearly = ex.createBook(siteout_path, vis)
    # wb_yearly = ex.open_workbook(siteout_path, vis)

    # run through each site
    for site in sites:
    # for site in [sites[0]]:        
    # for site in []:    

        # wx_years = list(set(wx.data.index.year)) 

        #### do this comparison differently, to be more robust ####
        # if (not np.all(sorted(list(set(wx.data.index.year))) == site.sp.yrs)) or \
        #     (len(list(set(wx.data.index.year))) < len(site.sp.yrs)):
        #         logger.critical(site.name.upper() + \
        #             ': Missing weather data.')

        if len(list(set(site.wx.data.index.year))) < len(site.yrs):
                logger.critical(site.site_name.upper() + \
                    ': Missing weather data.')                
                # raise SystemExit

        for ayear in site.yrs:
            if ayear not in list(set(site.wx.data.index.year)):
                    logger.critical(site.site_name.upper() + \
                        ': Missing weather data.')                
                    raise SystemExit                 

        # for year in site.sp.yrs:
        #     if year not in wx.data.index.year:
        #         logger.critical('Weather year missing: ' + str(year))
        #         raise SystemExit                

        rind = 3
        for acrop in site.crops:
            if rind == 3:

                sname = site.site_name.replace(" ", "")
                sname = sname.replace(".", "")

                wx_type = os.path.splitext(site.wx_file)[0][site.wx_file.index('_')+1:]

                filename = '_'.join([
                    sname.upper(),
                    site.crop_param_name.replace(" ", "").upper(),
                    site.et_method.upper(),
                    wx_type.replace(" ", "").upper(),
                    site.wx_location.replace(" ", "").upper(),])

                sname_monthly = 'Monthly_' + filename
                sname_yearly = 'Yearly_' + filename            

                wb_monthly = None
                site_path = os.path.join(results_dir, sname_monthly + '.xlsx')

                if os.path.exists(site_path):
                    # wb_monthly = ex.open_workbook(site_path, vis)
                    # if wb_monthly == None:
                    #     logger.critical('Close workbook: '+sname_monthly + '.xlsx')
                    #     raise SystemExit
                    # else:
                    #     # wb_monthly.Close(0)
                    #     ex.close_workbook(wb_monthly, 0)
                    try:
                        os.remove(site_path)
                    except PermissionError:
                        logger.critical('Close workbook: ' + sname_monthly + '.xlsx')
                        raise SystemExit
                wbm_ex = excel.Excel(site_path, vis, create=True)
                wb_monthly = wbm_ex.wb
                # wb_monthly = ex.open_workbook(site_path, vis)

                wb_yearly = None
                siteout_path = os.path.join(results_dir, sname_yearly + '.xlsx')

                if os.path.exists(siteout_path):
                    # wb_yearly = ex.open_workbook(siteout_path, vis)
                    # if wb_yearly == None:
                    #     logger.critical('Close workbook: '+ sname_yearly + '.xlsx')
                    #     raise SystemExit
                    # else:
                    #     # wb_yearly.Close(0)
                    #     ex.close_workbook(wb_yearly, 0)
                    try:
                        os.remove(siteout_path)
                    except PermissionError:
                        logger.critical('Close workbook: ' + sname_monthly + '.xlsx')
                        raise SystemExit
                wby_ex = excel.Excel(siteout_path, vis, create=True)
                wb_yearly = wby_ex.wb
                # wb_yearly = ex.createBook(siteout_path, vis)

                sheets = wb_yearly.Worksheets
                try:
                    ws = sheets(site.site_name)
                except:
                    ws = sheets.Add()
                    ws.Name = site.site_name

                headers = ['CU', 'Eff. P.', 'Net CU']
                units = [' (in.)', ' (ft.)']

                for i in range(3):
                    for j in range(2):
                        ws.Cells(rind, i+2+(3*j)).Value = headers[i] + units[j]
                ws.Range(ws.Cells(rind, 1), ws.Cells(rind, 7)).Font.Bold = True

            # instantiate a crop class object
            # try:
            #     ind = crp_classes.index(crop.name)
            #     crp = crp_classes[ind](crop, site, wx)

            # except Exception as err:
            #     logger.exception('Error occurred creating site object: ' 
            #         + site.name 
            #         + ', ' + crop)
            #     # logger.critical('traceback:' + str(err))
            #     raise

            # calculate consumptive use
            try:
                acrop.cu.calc_cu()
            except Exception as err:
                logger.exception('Error occurred calculating consumptive use')
                # logger.critical('traceback:' + str(err))
                raise  

            # print(acrop.__dict__)

            try:
                write_excel_monthly(
                                    wb_monthly,
                                    site.site_name,
                                    site.et_method,
                                    acrop,
                                    site.yrs,
                                    [acrop.cu.ppcu, acrop.cu.ppre, acrop.cu.pcuir],
                                    acrop.cu.grow_dates,
                                    acrop.cu.beg,
                                    acrop.cu.end,)
                write_excel_yearly(
                                    wb_yearly,
                                    site.site_name,
                                    site.et_method,
                                    acrop,
                                    site.yrs,
                                    [acrop.cu.ppcu, acrop.cu.ppre, acrop.cu.pcuir],
                                    acrop.cu.grow_dates,
                                    acrop.cu.beg,
                                    acrop.cu.end,
                                    rind)
                rind += len(site.yrs) + 2
            except Exception as err:
                logger.exception('Error occurred writing outfiles')
                # logger.critical('traceback:' + str(err))
                raise     

            # site summarize site wide variable for each variable for each month
            for yr in range(len(site.yrs)):
                for k in range(13):
                    site.pcu[yr, k] += acrop.cu.pcu[yr, k]
                    site.pre[yr, k] += acrop.cu.pre[yr, k]
                    site.pcuirr[yr, k] += acrop.cu.pcuirr[yr, k]

        wbm_ex.close_workbook(1)
        wby_ex.close_workbook(1)
        # ex.close()

        logger.info('finished with run for: ' + site.site_name)

    # ex.close()

    logger.info('CONS2 Finished')
    


def main():
    
    run()

if __name__=='__main__':
        try:
            main()
        except Exception as err:
            logger.exception('Error occurred in main()')
            raise



