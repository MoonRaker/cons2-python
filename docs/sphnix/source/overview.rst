.. _overview:

Overview
========

Introduction
------------

This is a Python based program used to caclulate monthly and yearly consumptive use based on the Blaney-Criddle method. It was written by Derek Groenendyk while at the United States Geological Survey at the Tucson Arizona Water Science Center Water Use Program and was created from an existing FORTRAN based program. The program has gone through several iterations. It currently allows for the calculation of  consumptive using two different Blaney-Criddle methods, one using  coeffiecients from the NRCS-SCS [USDA70]_ and another using Penman-Montieth coefficients from the FAO [DOO75]_. It requires only temperature and precipitation data to run. It currently assumes the use of PRISM or AZMET data, although data from another source of the same format could be easily substituted. Many of the crop parameters have been adjusted for use in Arizona.


Implementation
--------------

cons2-python has procedural code that runs using a library built around several classes. This procedural code and corrsponding scripts have been compiled into a single executable. However, it is possible to run using the procedural code and classes for those users who prefer to use Python and object-oriented programming.

.. _development_history:

Development History
-------------------

The XCONS was the program originally written by Joe Wensman of the Bureau of Reclamation. It was later modified by the Bureau of Reclamation and renamed XCONS2. It was obtained by David Anning of the United States Geological Survey Arizona Water Science Center on June 10th, 1994 courtesy of Conrad Jordheim at the Bureau of Reclamation office Denver, CO. Greg Dewey also sent along a copy of the Plan of Study and Methods Manual for the Colorado River System Consumptive Uses and Losses Report 1985-1990 from July 1992. This report contains details the use and implementation of XCONS2.

In 2016 the Water Use Area of the Tucson, Arizona Water Science Center of United States Geological Survey developed a Python based XCONS2 program. The updated XCONS2 program included major changes to code structure and input and output files and also additional methods for calculating consumptive use. Development of the cons2-python was motivated by the desire for simplified input and output files but also to add modular capabilities to the program. Modular code structure through the use of classes allows for the addition of other methods to calculate consumptive use as well as additional crop types.

This newest version, cons2-python, implements the same methods used in XCONS2 to calculate consumptive use. It has been validated against XCONS2 and it was shown that their results are comparable.

One significant change for cons2-python was that it allows the use of either SCS method for calculating consumptive use or the use of method that is based on FAO crop coefficients [DOO75]_.


XCONS & XCONS2
^^^^^^^^^^^^^^
XCONS was the name of the original program used to calculate crop consumptive use.  The program is based upon the SCS Modified Blaney-Criddle evapotransipiration (ET) estimation model as presented in the U.S. Department of Agriculture Soil Conservation Service's Irrigation Water Requirements Technical Release No. 21 (TR 21, revised september 1970) [USDA70]_.  

XCONS was originally developed by Joe Wensman of the Pacific Northwest Regional Office, Bureau of Reclamation, Department of the Interior, as program consuse. It has since been modified several times. 

XCONS was acquired by D-752 or CRSS (Colorado River Simulation System) of the Bureau of Reclamation office in Denver in January, 1981 and modified slightly. These modifications allow for output of summary tables only and elimination of the season by season summaries, use of depths other than three inches for computation of effective precipitation, use of up to 100 years of data in the computations (as opposed to the original 60 year limit) and printing of years between 1900 and 1909. The resulting current executable version is called XCONS2.


XCONS2 Methods
^^^^^^^^^^^^^^

The format for the data files is very exact and it is simpler to edit an existing file than to create a new one.  At the beginning of the Fortran code for XCONS2 is the following explanation of the variables and their positions.

CROP
NUMBER	CROP NAME				DESCRIPTION
1	ALFALFA					CROPS 1 6 ARE PERENNIAL
2	GRASS PASTURE			CROPS WITH CROP GROWTH
3	ORCHARD WITHOUT COVER	STAGE COEFFICIENT CURVE
4	ORCHARD WITH COVER		VALUES ON THE 1ST AND 15TH
5	HOPS(EST)				OF EACH MONTH; ((CKCA(I,J),
6	GRAPES					J=1,25),I=1,5).
7	DRY BEANS
8	SPRING GRAIN
9	CORN, SILAGE
10	SUGAR BEETS				CROPS 7 20 ARE ANNUAL CROPS
11	IRISH POTATOES			WITH CROP GROWTH STAGE
12	SMALL VEGETABLES		COEFFICIENT CURVE VALUES AT
13	SWEET CORN				5 PERCENT OF GROWING SEASON
14	SNAP BEANS				INTERVALS;((CKCP(I,J),J=1,
15	CORN, GRAIN				21),I=7,20).
16	DRY PEAS
17	GREEN PEAS				CROP GROWTH STAGE COEFFICIENT
18	TOMATO			        CURVE VALUES TAKEN FROM SCS
19	WINTER WHEAT, FALL		TECH. REL. NO. 21, 1970,
20	WINTER WHEAT, SPRING	UNLESS (EST)	
	
The growing season is determined by considering three different parameters: beginning and ending mean air temperature of moisture use; beginning and ending day of growing season; and length of growing season.  The first set of values are the mean air temperature of earliest moisture use (NBTEMP) and mean air temperature of latest moisture use (NETEMP).  Both of these values are found in TR 21 table 3 page 13.  In the case of alfalfa, 28:math:'^{\circ}' was used as the ending temperature.  The table suggests using a 28:math:'^{\circ}' frost.  The actual frost date will be entered as the ending day of growth (MENDDA).  For the annual crops, the same procedure is used.

The second set of values are beginning month and day of growing season (MBEGMO-MBEGDA) and ending month and day of growing season (MENDMO-MENDDA).  These values are used when actual dates are known.  The beginning day is usually the planting date or can be the last day at a certain temperature, such as a 28:math:'^{\circ}' frost.  The ending day can be a harvest date or the first day at a certain temperature, such as a 28:math:'^{\circ}' frost as is the case with alfalfa.  In cases where temperature controls the growing season such as pasture, 1/1 (January 1) and 12/31 (December 31) are used for the dates so that they will not be more restrictive than the temperatures.

The final value is the length of growing season (NGROWS).  Several annual crops have a maximum number of days of growth until they quit using water.  Corn is an example.  These values were found in TR 21 TABLE 3 page 13.  For crops that do not have a maximum number of days of growth, 365 was used so that it would not be a restrictive value.

The program looks at each of these values to determine the start and end of moisture use.  The two parameters for the start of growth in the spring, NBTEMP and MBEGMO-MBEGDA, are compared to see which occurred latest, that being the most restrictive.  The same thing is done for the end of growth.  NETEMP and MENDMO-MENDDA are compared to see which occurred earliest.  The length of the moisture use period found thus far is compared to NGROWS.  If NGROWS is shorter, the moisture use period is the start of moisture use in the spring plus NGROWS.  Otherwise, the moisture use period is that found previously.  By using this procedure, the most restrictive moisture use period is found and used for the program.  An example follows demonstrating this procedure.

A corn crop in a certain area is always planted on May 7 and harvested on or after October 6.  The variables for beginning and end of growing season, MBEGMO-MBEGDA, MENDMO-MENDDA, would be set to 5-7 and 10-6, respectively.  The mean air temperature for the beginning and end of moisture use is 55:math:'^{\circ}'F and 45:math:'^{\circ}'F, so NBTEMP is 55 and NETEMP is 45.  The growing season length is 140 days so NGROWS is 140.  The program then uses a linear interpolation of the mean monthly temperature to determine a date for the NBTEMP and NETEMP values and converts these dates to Julian days.

The program searches and finds the day in the spring when the mean air temperature reaches 55F (NBTEMP) and the day in the fall when the mean air temperature reaches 45F (NETEMP).  These days are then converted to Julian days.

The next step is to compare the Julian day value for NBTEMP with that of MBEGMO-MBEGDA.  The largest is considered the starting day of moisture use in the spring.  For this example, we will assume that 5-7 (Julian day 127) is the largest.

The program then takes the Julian day value of NETEMP and compares it with that of MENDMO-MENDDA.  The lessor of these is considered to be the ending day of moisture use.  For this example, we will assume that 10-6 (Julian day 279) is the largest.  The difference between the starting and ending days of moisture use (279-127=152) is compared to NGROWS (140).  If NGROWS is larger, the moisture use period is the beginning and ending days found previously (5-7 and 10-6).  Otherwise, as is this example, the moisture use season is the beginning day (5-7 or 127) plus NGROWS (127+140=267).  Julian day 267 corresponds to September 24.  The moisture use period for this example will be from May 7 to September 24.

This procedure produces the shortest growing season for that crop for that year.

Other variables that are input to the program:

The values for PCLITE, the monthly percentage of daylight hours, entered into the data file, are found in TR 21 TABLE 1 page 9.  For numbers not listed, a linear interpolation is used to match the latitude and this value is multiplied by 100.  The latitude is a weighted average of the latitudes of the weather stations used.  For example, the January value for a site at 38 degrees 31 minutes North latitude would be 684.

The values for PCCROP, percentage of project area for crop, will be a number between 1 and 1000 instead of 1 and 100.  For example, 43 percent is entered as 430.

It is important that the data file be in a DOS text format and that the margins are set to zero.  All data MUST be in the proper column for the program to operate correctly.  Normal nomenclature would put a DAT extension to the filename.


References
----------	

.. [USDA70] USDA SCS (U. S. Department of Agriculture, Soil Conservation Service). 1970. Irrigation Water Requirements. Technical Release No. 21. (rev.) 92 p. 

.. [DOO75] Doorenbos, J. and Pruitt, W.O.1975. Guidelines for predicting crop water requirements. Irrigation and drainage paper FAO No. 24 p195. 


Getting support
---------------
The best way to get support is to make an issue on our
`GitHub issues page <https://github.com/MoonRaker/cons2-python/issues>`_ .


How do I contribute?
--------------------
We're so glad you asked! Please see our
`wiki <https://github.com/MoonRaker/cons2-python/wiki/Contributing-to-pvlib-python>`_
for information and instructions on how to contribute.


Credits
-------
USGS Arizona Water Science Center Water Use Program for funding and support.
