.. _input_files:

Input Files
===========

There are at least two files required by cons2-python to run. A single file that is named sites_in.xlsx and contains the sites and corresponding site information for which consumptive use will be calculated. The rest are also .xlsx files that begin with "wx_" and contain the weather data needed by the Blaney-Criddle method. The name of these weather files are defined within the sites_in.xlsx file.

Sites File
----------

File must be name sites_in.xlsx and is required. This file is a Microsoft Excel spreadsheet in which each tab corresponds to a location or site for which consumptive is to be calculated. cons2-python will read each tab in this file and if there are no errors will calculate consumptive use for each of them. There are no formatting restrictions for the names of the tabs or sites. 

.. figure: /images/sites_in.png
   :scale: 50 %
   :alt: sample sites_in.xlsx spreadsheet

   Sample sites_in.xlsx spreadsheet.

Site Parameters
^^^^^^^^^^^^^^^

HUC : string, optional
	Hydrologic Unit Code for site, descriptive use only.

County : string, optional
	County where site is located, descriptive use only.

State : string
	State where site is located, descriptive use only.

NPRE : integer
	Method for computing effective precipitation. 1 for SCS, 2 for USBR. 

NBEGYR : integer
	Year in which calculation of consumptive use begins.

NENDYR : integer
	Year in which calculation of consumptive use ends.

APDEP : float
	Application depth in inches for computation of effective precipitation.

wx_type : string
	Filename for weather file.

wx_location : string
	Name corresponding to the location of the weather data to be used.
	
wx_units : string
	English or Metric

crop_parameters : string
	Set of crop parameters to be used, must be present in the parameter file corresponding to the ET method.

ET_method : string
	Blaney-Criddle method used to calculate consumptive use. Options are either "fao" or "scs". This value also determines which set of crop_parameters, which are contained in two separate files.


Weather File
------------

At least one weather file is required and the name(s) is set in the sites file. This file(s) is a Microsoft Excel spreadsheet in which each tab corresponds to weather data for a specific location or site. The year and month should always be the first two columns. Data required for calculation of consumptive use with Blaney-Criddle are precipitation and average temperature. The other mandatory fields are "Precipitation" and "Temp_Avg". They can appear in any order and are not case sensitive.

.. figure: /images/wx_data.png
   :scale: 50 %
   :alt: sample weather spreadsheet

   Sample weather spreadsheet.

Weather Data Inputs
^^^^^^^^^^^^^^^^^^^
   
Precipitation : float
	Total monthly precipitation by year.

Temp_Avg : float
	Daily average temperature averaged monthly by year.
	
cons2-python will read each tab in this file and if there are no errors will calculate consumptive use for each of them. There are no formatting restrictions for the names of the tabs or sites. 