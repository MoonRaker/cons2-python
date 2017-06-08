.. _output_files:

Output Files
============

cons2-python produces two output files containing consumptive use information. One file produces total consumptive use for the year and the other monthly consumptive use. Both files are in Microsoft Excel format. The file names assigned to each output file are unique to a location in the sites_in.xlsx input file.

Yearly
------

Consumptive use and effective precipitation values are provided in both inches and feet. Net consumptive use in simply the consumptive use less the effective precipitation. These values for each crop are listed by year. Also listed are average values, which are based on the yearly data. Each are rounded to two decimal places. The season type and KcNum used are also listed for each crop.

The yearly file naming convention is as follows:
Yearly_[SiteName]_[CropParametersLocation]_[ETMethod]_[WeatherType]_[WeatherLocation].xlsx

These values are set in the sites file, sites_in.xlsx.

.. figure: /images/yearly.png
   :scale: 50 %
   :alt: yearly output spreadsheet.

   Sample yearly output.


Monthly
-------

Consumptive use and effective precipitation values are provided in both inches and feet. Net consumptive use in simply the consumptive use less the effective precipitation. Each tab within the spreadsheet corresponds to a single crop. With each value broken down by year and month and averaged by year and month as well. Each value is rounded to two decimal places. The season type and KcNum used are also listed for each crop, along with growing season information for each year.

The monthly file naming convention is as follows:
Monthly_[SiteName]_[CropParametersLocation]_[ETMethod]_[WeatherType]_[WeatherLocation].xlsx

These values are set in the sites file, sites_in.xlsx.

.. figure: /images/monthly.png
   :scale: 50 %
   :alt: monthly output spreadsheet.

   Sample monthly output.