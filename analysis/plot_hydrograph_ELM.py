#%%
import numpy as np
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
from pfspinup import pfio
from pfspinup.common import calculate_surface_storage, calculate_subsurface_storage, calculate_water_table_depth, \
    calculate_evapotranspiration, calculate_overland_flow_grid
from pfspinup.pfmetadata import PFMetadata
import pandas as pd
import sys
from datetime import datetime, timedelta
import pytz
# from pyproj import Proj, transform
from scipy.stats import spearmanr

#%%
# RUN_DIR='USGS_Bedrock/year1'
# RUN_NAME='icom_USGS_bedrock'
RUN_DIR = sys.argv[1]
RUN_NAME = sys.argv[2]
#RUN_DIR='USGS'
#RUN_NAME='icom_USGS'
t_start = '2002-10-1'
obs='selected_gages.csv'
# obs_flow = '/Users/junzhang/Documents/ICOM/Data/Streamflow/icom_WY2003_daily_discharge.csv'
# stn_info = '/Users/junzhang/Documents/ICOM/Data/Streamflow/gage_info_icom_updated.csv'
# region_file = 'Regions.tif'

# RUN_DIR = sys.argv[1]
# RUN_NAME = sys.argv[2]
# t_start = sys.argv[3]
# obs = sys.argv[4]

#RUN_DIR='USGS_GLHYMPHS2_FBz'
#RUN_NAME='USGS_GLHYMPS2_FBz'
#t_start = '1982-10-1'
# obs = 'historical_data_1982_2019.csv'
#region_file = 'Regions.tif'
#%%
metadata = PFMetadata(f'{RUN_DIR}/{RUN_NAME}.out.pfmetadata')

# ------------------------------------------
# Get relevant information from the metadata
# ------------------------------------------

# Resolution
dx = metadata['ComputationalGrid.DX']
dy = metadata['ComputationalGrid.DY']
# Thickness of each layer, bottom to top
dz = metadata.dz()

# Extent
nx = metadata['ComputationalGrid.NX']
ny = metadata['ComputationalGrid.NY']
nz = metadata['ComputationalGrid.NZ']

# ------------------------------------------
# Get numpy arrays from metadata
# ------------------------------------------

# ------------------------------------------
# Time-invariant values
# ------------------------------------------
porosity = metadata.input_data('porosity')
specific_storage = metadata.input_data('specific storage')
mask = metadata.input_data('mask')

mask[np.isnan(mask)] = 0 #change mask value from nan to 0
mask[mask != 0] = 1 #change mask value from 99999 to 1
# Note that only time-invariant ET flux values are supported for now
#et_flux_values = metadata.et_flux()  # shape (nz, nx, ny) - units 1/T.

slopex = metadata.slope_x()  # shape (nx, ny)
slopey = metadata.slope_y()  # shape (nx, ny)
# mannings = metadata.get_single_domain_value('Mannings') # scalar value
# mannings = metadata.get_single_domain_value('Mannings')   
mann_file = metadata['Mannings.FileName']
mannings = pfio.pfread(f'{RUN_DIR}/{mann_file}').squeeze(axis=0)
## Flip the array upside down
#slopex = slopex[::-1, :]
#slopey = slopey[::-1, :]
#mask = mask[:, ::-1, :]


#%%
# ------------------------------------------
# Time-variant values
# ------------------------------------------
# Get as many pressure files as are available, while also getting their corresponding index IDs and timing info
pressure_files, index_list, timing_list = metadata.output_files('pressure', ignore_missing=True)

#we get the hour #14 of each day (i.e. 2pm MT)
xi = 14
t_start = '2002-10-1'
#generate a list of date
t_start = datetime.strptime(t_start,'%Y-%m-%d')
t_start = t_start.astimezone(pytz.UTC)
dt = int(timing_list[-1]) 
# dt = 24
#t_end = t_start + timedelta(hours=dt)
list_dates_dt = np.arange(xi,dt,24)
list_dates = [np.datetime64(
                (t_start.astimezone(pytz.timezone('America/New_York'))+\
                      timedelta(hours=int(x))).date()) for x in list_dates_dt]


# no. of time steps
nt = len(list_dates_dt)

#%%
# ------------------------------------------
# Initialization
# ------------------------------------------
# Arrays for total values (across all layers), with time as the first axis
overland_flow = np.zeros((nt, ny, nx))
ovld_flow_temp = np.zeros((ny, nx))
#%%
# ------------------------------------------
# Loop through time steps
# ------------------------------------------
idx = 0
for i, pressure_file in enumerate(pressure_files):
	dt = timing_list[i]
	curr_time = t_start+timedelta(hours=int(dt+xi))
	local_time = curr_time.astimezone(pytz.timezone('America/New_York'))
	np_time = np.datetime64(local_time)
	if np_time not in [x for x in list_dates]:
		continue
	pressure = pfio.pfread(pressure_file)
	#pressure = pressure[:, ::-1, :]
	pressure[mask == 0] = np.nan
	# ovld_flow_temp = calculate_overland_flow_kinematic(mask, pressure, slopex, slopey, mannings, dx, dy)
	ovld_flow_temp= calculate_overland_flow_grid(pressure, slopex, slopey, mannings, dx, dy, mask=mask)
	overland_flow[idx, ...] = ovld_flow_temp

	# overland_flow[idx, ...] = calculate_overland_flow_kinematic(mask, pressure, slopex, slopey, mannings, dx, dy)

	idx += 1

# overland_flow2 = calculate_overland_flow_kinematic(mask, pressure, slopex, slopey, mannings, dx, dy)
# overland_flow[idx,...]=overland_flow2

#%%
# print('overland_flow',np.max(overland_flow))
# print('ovld_flow_temp:',np.max(ovld_flow_temp))
# print('overland_flow2:',np.max(overland_flow2))
#%%

# overland_flow3 = overland_flow2.copy()
# overland_flow3=overland_flow3[::-1, :]
# print(overland_flow3[373,253])

# plt.clf()
# plt.imshow(overland_flow2)
# # plt.imshow(overland_flow[0,:,:])
# plt.imshow(overland_flow3)

# fig_name = 'overland.png'
# plt.savefig(fig_name)
#%%
overland_flow = overland_flow[:, ::-1, :]
#compare with observations
obs_df = pd.read_csv(obs)
obs_df['date'] = pd.to_datetime(obs_df['date'])

groups = obs_df.groupby('id')

out_list = []
for ii,group in groups:
	group = group[group['date'].isin(pd.to_datetime(list_dates))]
	group = group.sort_values('date')
	if group.empty:
		continue
	obs_value = np.array(group.value).astype(np.float32) * 0.0283 * 3600
	lon,lat = np.array(group.lon)[0],np.array(group.lat)[0]
	# x = int(np.array(group.x_new)[0])
	# y = int(np.array(group.y_new)[0])
	x = int(np.array(group.x)[0])
	y = int(np.array(group.y)[0])
	sel_idx = [kk for kk,zz in enumerate(list_dates) if \
				str(zz) in group.date.dt.strftime('%Y-%m-%d').tolist()]
	# sim_value = overland_flow[sel_idx, y, x]
	sim_value = overland_flow[sel_idx, x, y]
	columns = group.columns.tolist()
	columns[-1] = 'sim_value'
	out_df = pd.DataFrame(columns=columns)
	out_df['date'] = group.date
	out_df['id'] = group.id.iloc[0]
	out_df['lat'] = lat
	out_df['lon'] = lon
	out_df['x'] = x
	out_df['y'] = y
	out_df['value'] = obs_value
	out_df['site_name'] = group.site_name.iloc[0]
	out_df['sim_value'] = sim_value
	out_list.append(out_df)

out_df = pd.concat(out_list,ignore_index=True)

out_df.to_csv(RUN_NAME+'.csv', index=False)

fig, axs = plt.subplots(np.int(np.ceil(len(out_list) / 3)),3, figsize=(20,10))

for ii, outi  in enumerate(out_list):
	ax = axs[ii // 3, ii % 3]
	ax.set_title(outi.site_name.iloc[0], fontsize = 18)
	ax.plot(outi.value, 'r', label = 'observation')
	ax.plot(outi.sim_value, 'b', label = 'simulation')

	#statistic calculation
	spearmanr_temp = np.round(spearmanr(outi.value, outi.sim_value)[0],2)
	bias_temp = np.round(((np.nansum(outi.value) - np.nansum(outi.sim_value)) / np.nansum(outi.value)),3)*100
	loc_10th = np.where(outi.value>(np.percentile(outi.value,10)))
	value_10th_obs = np.asarray(outi.value)[loc_10th]
	value_10th_sim = np.asarray(outi.sim_value)[loc_10th]
	spearmanr_10th = np.round(spearmanr(value_10th_obs, value_10th_sim)[0],2)

	loc_90th = np.where(outi.value>(np.percentile(outi.value,90)))
	value_90th_obs = np.asarray(outi.value)[loc_90th]
	value_90th_sim = np.asarray(outi.sim_value)[loc_90th]
	spearmanr_90th = np.round(spearmanr(value_90th_obs, value_90th_sim)[0],2)

	plot_value = np.nanmax([np.nanmax(outi.value),np.nanmax(outi.sim_value)])
	ax.text((10 + 365*ii), plot_value*0.9, 'spearmanr:' + str(spearmanr_temp), size = 15)
	ax.text((10 + 365*ii), plot_value*0.75, 'bias:' + str(bias_temp) + '%', size = 15)
	ax.text((10 + 365*ii), plot_value*0.6, 'over 10th spr:' + str(spearmanr_10th), size = 15)
	ax.text((10 + 365*ii), plot_value*0.45, 'over 90th spr:' + str(spearmanr_90th), size = 15)

	if (ii % 3) == 0:
		ax.set_ylabel('Discharge cmh')
	handles, labels = ax.get_legend_handles_labels()

fig.legend(handles, labels)
fig.tight_layout(pad=1.0)
fig.savefig(RUN_NAME+'.png')











