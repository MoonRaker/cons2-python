.. _input_files:

Input Files
===========

There are at least two files required by CONS2 to run. A single file that is named sites_in.xlsx and contains the sites and corresponding site information for which consumptive use will be calculated. The rest are also .xlsx files that begin with "wx_" and contain the weather data needed by the Blaney-Cridle method. The name of these weather files are defined within the sites_in.xlsx file.

sites_in.xlsx
-------------

This file is a Microsoft Excel spreadsheet in which each tab corresponds to a location or site for which consumptive is to be calculated. CONS2 will read each tab in this file and if there are no errors will calculate consumptive use for each of them. There are no formatting restrictions for the names of the tabs or sites. 


Site Parameters
...............

HUC
Descriptive, Non-mandatory, String: Hydrologic Unit Code for site. 

County
Descriptive, Non-mandatory, String: County where site is located.

State
Descriptive, Non-mandatory, String: State where site is located.

NOUT
Non-mandatory, Integer: Number of 

NPRE
Non-mandatory, Integer: Number of 

NBEGYR
Mandatory, Integer: Year in which calculation of consumptive use begins.

NENDYR
Mandatory, Integer: Year in which calculation of consumptive use ends.

APDEP
Non-Mandatory, Integer: Unused.

wx_type
Mandatory, string: Filename for weather file.

wx_location
Mandatory, string: Name corresponding to the location of the weather data to be used.

crop_parameters
Mandatory, string: Set of crop parameters to be used, must be present in the ET specific file.

ET_method
Mandatory, string: Blaney-Cridle method used to calculate consumptive use. Options are either "fao" or "scs". This value also determines which set of crop_parmaters, which are contained in two separate files.


wx_%type%.xlsx
--------------

This file is a Microsoft Excel spreadsheet in which each tab corresponds to weather data for a specific location or site. The year and month should always be the first two columns. Data required for calculation of consumptive use with Blaney-Cridle are precipitation and average temperature. The other mandatory fields are "Precipitation" and "Temp_Avg". They can appear in any order and are not case sensitive.

To weather types are supported. 



, Precipitation, Temp_Avg. 


CONS2 will read each tab in this file and if there are no errors will calculate consumptive use for each of them. There are no formatting restrictions for the names of the tabs or sites. 






Reference Files
===============

crop_coef_ckc.csv

crop_coef_nckc.csv

crop_dev_coef.csv

crop_parameters_fao.xlsx

crop_parameter_scs.xlsx

crop_ref.csv




