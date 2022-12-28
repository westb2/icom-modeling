#%%
import os
import numpy as np
import gdal
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly as py
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import sys
import pandas as pd
from pfspinup import pfio
from pfspinup.pfmetadata import PFMetadata
from pfspinup.common import calculate_surface_storage, calculate_subsurface_storage, calculate_water_table_depth, \
    calculate_evapotranspiration, calculate_overland_flow_grid

#%%
# indirs = ['/glade/scratch/junzhang55/icom/Final_SUB','/glade/scratch/junzhang55/icom/CLM_P_ET_runs']
# runs  = ['G1_Multi_EF_ShgFBz_200m_kz01_rv50_dec_mann_25inc','CLM_P_ET_WY2003']
# labels = ['clm_cp','clm_pet']

# indirs = ['/glade/scratch/junzhang55/icom/CLM_P_ET_runs']
# runs  = ['CLM_P_ET_WY2003']
# labels = ['clm_pet']

# indirs = ['/glade/scratch/junzhang55/icom/ELM_run_no_negative']
# runs  = ['ELM_PET_no_negative']
# labels = ['ELM_no_negative']

indirs = ['/global/cscratch1/sd/jzhang55/ELM_running/runs/ELM_07232021']
runs  = ['ELM_re1']
labels = ['fixed_FB']

run_no = len(runs)

# substor_all = np.zeros((run_no,nt))
# surfstor_all = np.zeros((run_no,nt))
# et_all = np.zeros((run_no,nt))
for ii,indir in enumerate(indirs):
	# print(ii)
	# print(indir)
	runname = runs[ii]
	label = labels[ii]
	metadata = PFMetadata(f'{indir}/{runname}.out.pfmetadata')

	# Resolution
	dx = metadata['ComputationalGrid.DX']
	dy = metadata['ComputationalGrid.DY']
	# Thickness of each layer, bottom to top
	dz = metadata.dz()

	# Extent
	nx = metadata['ComputationalGrid.NX']
	ny = metadata['ComputationalGrid.NY']
	nz = metadata['ComputationalGrid.NZ']

	porosity = metadata.input_data('porosity')
	specific_storage = metadata.input_data('specific storage')
	mask = metadata.input_data('mask')
	# Note that only time-invariant ET flux values are supported for now
	# et_flux_values = metadata.et_flux()  # shape (nz, ny, nx) - units 1/T.

	# slopex = metadata.slope_x()  # shape (ny, nx)
	# slopey = metadata.slope_y()  # shape (ny, nx)
	# mannings = metadata.get_single_domain_value('Mannings')  # scalar value

	# Get as many pressure files as are available, while also getting their corresponding index IDs and timing info
	pressure_files, index_list, timing_list = metadata.output_files('pressure', ignore_missing=True)
	# We're typically interested in the first value of the returned 3-tuple.
	# Note that if we were interested in specific time steps, we can specify these as the `index_list` parameter.
	# examples:
	#   files, _, _ = metadata.output_files('pressure', index_list=range(0, 31, 10))
	#   files, _, _ = metadata.output_files('pressure', index_list=[10, 30])

	# By explicitly passing in the index_list that we obtained in the call below,
	# we insist that all saturation files corresponding to the pressure files be present.
	saturation_files, _, _ = metadata.output_files('saturation', index_list=index_list)
	# no. of time steps
	nt = len(index_list)

	subsurface_storage = np.zeros(nt)
	surface_storage = np.zeros(nt)
	wtd = np.zeros((nt, ny, nx))
	et = np.zeros(nt)
	overland_flow = np.zeros((nt, ny, nx))

	for i, (pressure_file, saturation_file) in enumerate(zip(pressure_files, saturation_files)):
		pressure = metadata.pfb_data(pressure_file)
		saturation = metadata.pfb_data(saturation_file)

		# total subsurface storage for this time step is the summation of substorage surface across all x/y/z slices
		subsurface_storage[i, ...] = np.sum(
			calculate_subsurface_storage(porosity, pressure, saturation, specific_storage, dx, dy, dz, mask=mask),
			axis=(0, 1, 2)
		)

		# total surface storage for this time step is the summation of substorage surface across all x/y slices
		surface_storage[i, ...] = np.sum(
			calculate_surface_storage(pressure, dx, dy, mask=mask),
			axis=(0, 1)
		)

		# wtd[i, ...] = calculate_water_table_depth(pressure, saturation, dz)

		# if et_flux_values is not None:
		# 	# total ET for this time step is the summation of ET values across all x/y/z slices
		# 	et[i, ...] = np.sum(
		# 		calculate_evapotranspiration(et_flux_values, dx, dy, dz, mask=mask),
		# 		axis=(0, 1, 2)
		# 	)
			# et_all[ii,:] = et

	np.save('subsurface_storage.npy',subsurface_storage)
	np.save('surface_storage.npy',surface_storage)
	np.save('et.npy',et)
	print('calculation done!')
	df = pd.DataFrame()
	df['surf_stor'] = surface_storage
	df['sub_stor'] = subsurface_storage
	df['et'] = et

	df.to_csv(label+'_stor.csv')
	print(str(ii)+'saved!')
	# substor_all[ii,:] = subsurface_storage
	# surfstor_all[ii,:] = surface_storage


		# overland_flow[i, ...] = calculate_overland_flow_grid(pressure, slopex, slopey, mannings, dx, dy, mask=mask)