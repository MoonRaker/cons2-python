.. currentmodule:: cons2

#############
API Reference
#############

Classes
=======

pvlib-python provides a collection of classes for users that prefer
object-oriented programming. These classes can help users keep track of
data in a more organized way, and can help to simplify the modeling
process. The classes do not add any functionality beyond the procedural
code. Most of the object methods are simple wrappers around the
corresponding procedural code.

.. autosummary::
	:toctree: generated/
	
	cu.CONSUMPTIVE_USE
	crop.CROP
	site.SITE
	weather.WEATHER
	excel.Excel

cu.CONSUMPTIVE_USE
------------------

CONSUMPTIVE_USE Class definitions.

.. autosummary::
	:toctree: generated/
   
	cu.CONSUMPTIVE_USE.__init__
	cu.CONSUMPTIVE_USE.calc_adj
	cu.CONSUMPTIVE_USE.calc_cu
	cu.CONSUMPTIVE_USE.calc_dates
	cu.CONSUMPTIVE_USE.calc_effprecip
	cu.CONSUMPTIVE_USE.calc_fao
	cu.CONSUMPTIVE_USE.calc_faokc
	cu.CONSUMPTIVE_USE.calc_kc
	cu.CONSUMPTIVE_USE.calc_midpts
	cu.CONSUMPTIVE_USE.calc_pclite
	cu.CONSUMPTIVE_USE.calc_temp
	cu.CONSUMPTIVE_USE.clndr
	cu.CONSUMPTIVE_USE.fall
	cu.CONSUMPTIVE_USE.fao_cu
	cu.CONSUMPTIVE_USE.fiveyr_avg
	cu.CONSUMPTIVE_USE.get_dates
	cu.CONSUMPTIVE_USE.interp_kc
	cu.CONSUMPTIVE_USE.jln
	cu.CONSUMPTIVE_USE.kc_ann
	cu.CONSUMPTIVE_USE.kc_per
	cu.CONSUMPTIVE_USE.midday
	cu.CONSUMPTIVE_USE.midtemp
	cu.CONSUMPTIVE_USE.mmtemp
	cu.CONSUMPTIVE_USE.set_dates
	cu.CONSUMPTIVE_USE.spring

	
crop.CROP
---------

CROP Class definitions.

.. autosummary::
	:toctree: generated/
  
	crop.CROP.__init__
	crop.CROP.get_ckc
	crop.CROP.get_nckc
	crop.CROP.read_cropdev
	crop.CROP.read_kc
	crop.CROP.read_stages

	
weather.WEATHER
---------------

WEATHER Class definitions.

.. autosummary::
	:toctree: generated/
   
	weather.WEATHER.__init__
	weather.WEATHER.mnmnthly
	weather.WEATHER.read_data
	
	
site.SITE
---------

SITE Class definitions.

.. autosummary::
	:toctree: generated/
	
	site.SITE.__init__
	site.SITE.import_crops
	site.SITE.read_cropfile
	site.SITE.read_sitefile
	
	
excel.Excel
-----------

SITE Class definitions.

.. autosummary::
	:toctree: generated/  
	
	excel.Excel.__init__
	excel.Excel.close_workbook
	excel.Excel.createSheet
	excel.Excel.create_workbook
	excel.Excel.open
	excel.Excel.open_workbook
	excel.Excel.setVis	
	
Main
====
   
.. autosummary::
	:toctree: generated/
	
	main
	

main
----

.. autosummary::
	:toctree: generated/ 
	
	main.import_data
	main.main
	main.run
	main.write_crp_output
	main.write_excel_monthly
	main.write_excel_yearly
	main.write_output	
	
	
Read Infile
===========


.. autosummary::
	:toctree: generated/
	
	read_infile
		
	
	
	

	



	
