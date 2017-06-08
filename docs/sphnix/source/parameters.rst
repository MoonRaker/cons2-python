.. _parameters:

Parameter Files
===============

scs_crop_stages.csv
-------------------

.. figure: /images/scs_crop_stages.png
   :scale: 50 %
   :alt: scs crop growth stages

   SCS crop growth stages. Annual crops have 25 stages that occur on the 1st and 15th of each month. Perennial crops have 21 stages based on a 5 percent intervals for the length of the growing season.
   
scs_crop_stage : integer
	SCS crop growth stages for annual and perennial crops.  
	

scs_crop_coef.csv
-----------------

.. figure: /images/scs_crop_coef.png
   :scale: 50 %
   :alt: scs crop coefficients

   SCS crop growth coefficients. Annual have 25 coefficients that occur on the 1st and 15th of each month. Perennial crops have 21 coefficients based on a 5 percent intervals for the length of the growing season.
   
scs_crop_coef : float
	SCS crop growth coefficients for annual and perennial crops.
	

fao_crop_stages.csv
-------------------

.. figure: /images/fao_crop_stages.png
   :scale: 50 %
   :alt: fao crop stages

   Crop growth stages as given by the FAO. Converted to decimal fraction of season. Stages must sum to equal 1.
   
season length : string
	Can be any value. Describes the type of season and corresponds to different crop growth stages.    

Lini : integer
	Decimal fraction of the initial growth stage.    

Ldev : integer
	Decimal fraction of the development growth stage.   

Lmid : integer
	Decimal fraction of the middle growth stage.   

Llate : integer
	Decimal fraction of the late growth stage.   	
	
   
fao_crop_coef.csv
-----------------

.. figure: /images/fao_crop_coef.png
   :scale: 50 %
   :alt: fao crop coefficients
   
   Crop growth coefficients as given by the FAO. 

Kcnum : integer
	Identifier for specific crop coefficients.   

Kini : float
	Coefficient for the initial crop growth stage.   

Kmid : integer
	Coefficient for the middle crop growth stage.   

Kend : integer
	Coefficient for the end of the season crop growth stage.    
 	
	
scs_crop_parameters.xlsx
------------------------

.. figure: /images/scs_crop_parameter.png
   :scale: 50 %
   :alt: scs crop parameters

   Each tab in this spreadsheet correspond to location specific crop parameters.

Crop Parameters : string
	Name of the crop. Must be present in SCS crop data files, scs_crop_coef.csv and scs_crop_stages.csv.    

NICKNAME : string, optional
	Alternate name of crop, not used, descriptive only.   

NBTEMP : integer
	Mean air temperature of earliest moisture use.   

NETEMP : integer
	Mean air temperature of latest moisture use.	
	
MBEGMO : integer
	Earliest month crop growth can begin.   

MBEGDA : integer
	Earliest day of month crop growth can begin.     

MEDNMO : integer, optional
	Month in which crop growth ends. Descriptive only and set internally based on NGROWS and NBEGMO and NBEGDA.   

MENDDA : integer, optional
	Day of month in which crop growth ends. Descriptive only and set internally based on NGROWS and NBEGMO and NBEGDA.
	
NGROWS : integer
	Number of days in growing season.    

PCLITE : float
	Monthly percentage of daylight hours for the year at a given latitude.
	
	
fao_crop_parameters.xlsx
------------------------

.. figure: /images/fao_crop_parameters.png
   :scale: 50 %
   :alt: fao crop parameters

   Each tab in this spreadsheet correspond to location specific crop parameters.

Crop Parameters : string
	Name of the crop. Must be present in FAO crop data files, fao_crop_coef.csv and fao_crop_stages.csv.  

NICKNAME : string
	Alternate name of crop, not used, descriptive only.   

MBEGMO : integer
	Earliest month crop growth can begin.   

MBEGDA : integer
	Earliest day of month crop growth can begin.     

MEDNMO : integer, optional
	Month in which crop growth ends. Descriptive only and set internally based on NGROWS and NBEGMO and NBEGDA.      

MENDDA : integer, optional
	Day of month in which crop growth ends. Descriptive only and set internally based on NGROWS and NBEGMO and NBEGDA.
	
NGROWS : integer
	Number of days in growing season.    

STYPE : string
	Type of growing season. Must match a season listed in fao_crop_stages.csv

KCNUM : integer
	Number identifying which crop coefficients to use. Must match a value in fao_crop_coef.csv

Latitude : float
	Latitude of site. Used to calculate monthly percentage of daylight hours.

	
crop_ref.csv
------------

.. figure: /images/crop_ref.png
   :scale: 50 %
   :alt: crop ref

   Reference containing specific crop parameters and values.

Short name : string
	Condensed and abbreviated name of crop.   

long name : string
	Full name of crop.

type : string
	Crop growth type. 

mmnum : integer
	Number of months used to find Spring mean temperature. SCS method only.
   
