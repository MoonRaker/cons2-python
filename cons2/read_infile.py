# read_infile.py
# Derek Groenendyk
# 5/3/2016
# reads xcons input files into dictionaries
"""


"""

from collections import OrderedDict
from itertools import islice
import numpy as np
import pandas as pd


def get_data(fname):

    site_names = ['NUCROPS', 'NOUT', 'NPRE', 'NBEGYR', 'NENDYR', 'APDEP']
    site_names = [item.lower() for item in site_names]

    with open(fname, 'r') as f:
        site_name = list(islice(f, 1))[0].strip().lower()
        site_name = site_name[0].upper() + site_name[1:]
        try:
            idx = site_name.index(' ') + 1
            site_name = site_name[:idx] + site_name[idx].upper() + site_name[idx+1:]
        except:
            pass
        list(islice(f, 2))
        site_vals = [float(item) for item in list(islice(f, 1))[0].split()]
        site_vals[:-1] = [int(item) for item in site_vals[:-1]]
        site_params = dict(zip(site_names, site_vals))
        site_params['site_name'] = site_name
        site_params['numyrs'] = int(site_params['nendyr'] \
            - site_params['nbegyr'] + 1)
        crop_params = OrderedDict()
        line = list(islice(f, 1))[0].split()
        while len(line) == 1:
            cname = line[0]
            sline = list(islice(f, 1))[0].split()
            param_vals = [int(sline[0])]
            [param_vals.append(int(item)) for item in sline[2:]]
            # param_vals[0] -= 1
            param_names = ['NCROP', 'NBTEMP', 'NETEMP', 'MBEGMO', 'MBEGDA',
                           'MENDMO', 'MENDDA', 'NGROWS']
            param_names = [item.lower() for item in param_names]
            crop_params[cname] = dict(zip(param_names, param_vals))
            line = list(islice(f, 1))[0].split()
        site_params['pclite'] = [float(item) / 100.0 for item in line]
        site_params['nts'], site_params['nps'] = [int(item) for item in \
                                            list(islice(f, 1))[0].split()]
        site_params['wts'] = float(list(islice(f, 1))[0].split()[0]) / 100.0
        site_params['wps'] = float(list(islice(f, 1))[0].split()[0]) / 100.0
        nyrs = site_params['nendyr'] - site_params['nbegyr'] + 1
        lines = list(islice(f, nyrs))
        temp = OrderedDict()
        for line in lines:
            sline = line.split()
            yr = sline[0]
            data = [float(item) for item in sline[1:]]
            temp[yr] = data
        site_params['temperature'] = pd.DataFrame(temp)
        precip = OrderedDict()
        for yr in range(nyrs):
            data = [float(item) for item in list(islice(f, 1))[0].split()]
            precip[list(temp.keys())[yr]] = data
        site_params['precip'] = pd.DataFrame(precip)

        # pccrop = OrderedDict()
        # areat = OrderedDict()
        # for yr in range(nyrs):
        #     data = [float(item) / 10.0 for item in list(islice(f, 1))[0].split()]
        #     pccrop[list(temp.keys())[yr]] = data
        #     data = [float(item) / 10.0 for item in list(islice(f, 1))[0].split()]
        #     areat[list(temp.keys())[yr]] = data
        pccrop = np.zeros((nyrs, site_params['nucrops']))
        areat = np.zeros((nyrs))
        for yr in range(nyrs):
            data = [float(item) / 10.0 for item in \
                list(islice(f,1))[0].split()]
            pccrop[yr, :] = data
            data = [float(item) / 10.0 for item in \
                list(islice(f,1))[0].split()]
            areat[yr] = data[0]
        site_params['areat'] = areat
        site_params['pccrop'] = pccrop
        line = list(islice(f, 1))[0]
        site_params['ibasin'] = line[:8].strip()
        site_params['cname2'] = line[8:23].strip()
        site_params['st'] = line[23:34].strip()

    return site_params, crop_params  


def main():

    fname = 'noga.i'

    site_params, crop_params = get_data(fname)

    print(crop_params)
    print(site_params)

if __name__=='__main__':
    main()