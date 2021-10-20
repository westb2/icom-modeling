
README
-------
This file contains a brief synopsis of the files contained within this folder. If it
is found to be incomplete, please reach out to jswilley@mymail.mines.edu with any 
questions.


Location
---------
/CONUS2.0/subsurface_development/Upper_DE_PFBs


General
--------
This folder contains ParFlow binary files that define the subsurface of the Upper Delaware
hydrologic model. Each file is a full and complete, multi-layer subsurface configuration
including soil and underlying geology. The geology of each subsurface configuration
may be defined by a single dataset or a combination. Cases that combine two datasets
will expressly state that they are a combination. 

The majority of datasets provided here contain indicator values and not actual hydraulic
conductivities. These indicators will need to be defined in you model's TCL script. 
The indicator parameter values can be changed, but a record is being kept of each
setup. This can be found here:

/CONUS2.0/subsurface_development/Testing_Record/CONUS_testing_2020.xlsx

Additionally, some subsurface files may contain actual hydraulic conductivity values.
These will need to be loaded into your slightly differently, but a note will be made 
alerting the modeler when this is the case.

For more information on the construction of each dataset and the input parameters, check
out this directory:
/CONUS2.0/subsurface_development/Hydrogeology_Workspace/


General
--------
This folder contains ParFlow binary files that define the subsurface of the CONUS 2.0
hydrologic model. Each file is a full and complete, multi-layer subsurface configuration
including soil and underlying geology. The geology of each subsurface configuration
may be defined by a single dataset or a combination. Cases that combine two datasets
will expressly state that they are a combination. 

The majority of datasets provided here contain indicator values and not actual hydraulic
conductivities. These indicators will need to be defined in you model's TCL script. 
The indicator parameter values can be changed, but a record is being kept of each
setup. This can be found here:

/CONUS2.0/subsurface_development/Testing_Record/CONUS_testing_2020.xlsx

Additionally, some subsurface files may contain actual hydraulic conductivity values.
These will need to be loaded into your slightly differently, but a note will be made 
alerting the modeler when this is the case.

For more information on the construction of each dataset and the input parameters, check
out this directory:
/CONUS2.0/subsurface_development/Hydrogeology_Workspace/


Files
------
All of the files contained within this folder should be listed and described here.

Analytical_K_case_1.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. Beneath that, hydraulic
	conductivity is defined by a Luo approach to hydraulic conductivity. Drainage density
	is used. Depth of incision and aquifer thickness are used to estimate hydraulic
	gradient. Aquifer thickness is assumed to be greater than or equal to 100m. This is a 
	K field and not an indicator field.
	
Analytical_K_case_7.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. Beneath that, hydraulic
	conductivity is defined by a Darcy approach to hydraulic conductivity. Average flow 
	length is used (Euclidean). Topographic slope from a USGS 30m DEM averaged at 250m
	and then again at the HUC12 level is used to estimate hydraulic gradient. 
	This is a K field and not an indicator field.
	
Analytical_K_case_9.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. Beneath that, hydraulic
	conductivity is defined by a Darcy approach to hydraulic conductivity. Average 
	surface flow length from the CONUS 2.0 grid is used. Topographic slope from the CONUS
	2.0 1Km grid is used to estimate hydraulic gradient. This is a K field and not an 
	indicator field.

GLHYMPS_1.0_Bedrock.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is GLHYMPS 1.0 mapped to CONUS indicators. Beneath that is an 
	indicator value of 19, which represents bedrock.

GLHYMPS_1.0_Efold.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. The geology here is defined by an 
	e-folded version of the  GLHYMPS 1.0 dataset.
	
GLHYMPS_1.0_USSG.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is GLHYMPS 1.0 mapped to CONUS indicators. Beneath that is the USGS
	primary aquifer and secondary hydrologic region map assigned CONUS indicators.

GLHYMPS_1.0.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. The geology here is defined by the 
	GLHYMPS 1.0 dataset.
	
GLHYMPS_2.0_Bedrock.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is GLHYMPS 2.0 mapped to CONUS indicators. Beneath that is an 
	indicator value of 19, which represents bedrock.
	
GLHYMPS_2.0_Efold.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. The geology here is defined by an 
	e-folded version of the  GLHYMPS 2.0 dataset.
	
GLHYMPS_2.0_GLHYMPS_1.0_EF.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is GLHYMPS 2.0 mapped to CONUS indicators. Beneath that is an e-floded
	version of GLHYMPS 1.0, which is largely bedrock after having been e-folded.
	
GLHYMPS_2.0_USSG.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is GLHYMPS 2.0 mapped to CONUS indicators. Beneath that is the USGS
	primary aquifer and secondary hydrologic region map assigned CONUS indicators.

GLHYMPS_2.0.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. The geology here is defined by the 
	GLHYMPS 2.0 dataset.
	
GLHYMPS_Study_Values.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is GLHYMPS 2.0 mapped to CONUS indicators. Beneath that is GLHYMPS 
	1.0. Here, GLHYMPS study values are used instead of CONUS indicators. This is a K 
	field and not an indicator field.
	
USGS_Bedrock.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is defined by our USGS dataset. This dataset is the combination of the 
	USGS primary aquifers and secondary hydrologic regions all mapped to CONUS 1.0 
	indicators by rock type. Beneath that is an indicator value of 19, which represents 
	bedrock.
	
USGS_GLHYMPS_1.0_EF.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. There are two different geology 
	sets beneath the soil disaggregated by Shangguan's estimates for depth to bedrock.
	The upper layer is defined by our USGS dataset. This dataset is the combination of the 
	USGS primary aquifers and secondary hydrologic regions all mapped to CONUS 1.0 
	indicators by rock type. Beneath that is the GLHYMPS 1.0 dataset with e-folding.
	
USGS.pfb
	This is a 10-layer subsurface with 4 of those layers being soil and the underlying 6
	being geology. The top three layers of soil are defined by one band of soil data, and 
	the other is defined by a second band of soil data. The geology is defined by our USGS
	dataset. This dataset is the combination of the USGS primary aquifers and secondary
	hydrologic regions all mapped to CONUS 1.0 indicators by rock type. Areas outside of
	the US border have been filled with GLHYMPS 1.0.
	
	
	