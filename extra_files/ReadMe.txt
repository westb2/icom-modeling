In this folder, there are some initial runs and processing scripts with ELM PET forcing data. Details are listed below.

./WY2003_forcing： contains ELM PET forcing data for ParFlow
	- *.pfb: PET in each time step (hourly), in total 8760 hours
	- Dist_Forcings_ELM.tcl: tcl script to distribute the forcing files with designated cores. The number of cores should be consistent with the number to run ParFlow. This distribution procedure should be done before running ParFlow. Use tclsh to run the script.
	- *.pfb.dist: distributed files from forcing data

./forcing_scripts: contains scripts to generate PET forcing data from ELM dataset
	- input_proc_cori.py: the main script to process PET forcing data. The original ELM dataset provides PET in a much larger domain and lower resolution. This script clips for the ICoM domain that we want and assigns each grid with the nearest value in the original dataset. The final forcing dataset is in 1km and hourly resolution.
	- check_forcing.py: this script checks the generated forcing data by calculating and plotting the spatial averaged PET and temporal averaged PET.
	- icom_locs.csv: the location inforamtion of all grids in lat/lon. Used in input_proc_cori.py.
	- write_pfb.py: a subfunction used in input_proc_cori.py to write pfb files.
	-  icom_rmcoast3.out.mask.pfb: the mask file used in input_proc_cori.py to clip out the values outside mask.
	- ./PF_Model_Evaluation: the github repo to install in python to run some modules. 
	
./runs: contiains an example run with WY2003 forcing data and some post-processing scripts
	- ./ELM_WY2003: an example run
		- icom_ELM.tcl: the main script to run the model
		- icom_ELM_re*.tcl: the script to restart the simulation if it's not done in one job
		- job_script: the script to submit the job
		- *.press.pfb: the pressure outputs
		- *.satur.pfb: the saturation outputs
		- *other files are either input files or model outputs for the performance, please refer to ParFlow manual for more details.
	- plot_hydrograph_ELM.py: script to calculate streamflow from selected gages.
	- selected_gages.csv: the selected gages with observed streamflow, used in plot_hydrograph_ELM.py.
	- wtd_calculation_pfspinup_1_0_2.py: script to calculate the water table depth from simulation
	- wells_take_mean_new.csv: wells locations and observations from Yin Fan's dataset. Used in wtd_calculation_pfspinup_1_0_2.py.
	- storage_comparison.py: script to calculate storage of each time step from the simulation.

