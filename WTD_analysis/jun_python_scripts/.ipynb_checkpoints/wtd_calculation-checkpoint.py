import os
#import matplotlib as mpl
#mpl.use('Agg')
#import matplotlib.pyplot as plt
#import pandas as pd
import numpy as np
from glob import glob
from datetime import datetime, timedelta
import pytz
#from scipy.stats import spearmanr
#import pfio
from parflowio.pyParflowio import PFData
import sys

# sim_year = sys.argv[1]
# sim_year = int(sim_year)

sim_year = 2003
indir = 'USGS'
out_name = indir + '_wtd'
# indir = sys.argv[2]
# if indir[-1] == '/':
#         indir = indir[:-1]

# out_name = None
# out_name = sys.argv[3]
# if out_name is None:
# 	out_name = indir

# start time of the simulation
t_start = datetime(sim_year-1,10,1,6,0,0,0,pytz.UTC)

#get all the pressure and saturation files in the specified directory
press_files = sorted(glob(indir+'/*.out.press.*.pfb'))
satur_files = sorted(glob(indir+'/*.out.satur.*.pfb'))

#distance/depth from the center of layers to the surface
depth = {0:1192-500,
		1:1192-1000-50,
		2:1192-1000-100-25,
		3:1192-1000-100-50-12.5,
		4:1192-1000-100-50-25-5,
		5:1192-1000-100-50-25-10-2.5,
		6:1192-1000-100-50-25-10-5-0.5,
		7:1192-1000-100-50-25-10-5-1-0.3,
		8:1192-1000-100-50-25-10-5-1-0.6-0.15,
		9:0.05}

#snapshot at 2pm MDT
xi = 14

#generate a list of date
dt = int(os.path.basename(press_files[-1]).split('.')[-2]) 
t_end = t_start + timedelta(hours=dt)
list_dates_dt = np.arange(xi,dt,24)
list_dates = [np.datetime64(
                t_start.astimezone(pytz.timezone('America/New_York'))+\
                      timedelta(hours=int(x))) for x in list_dates_dt]

# specify the daily array
# total_arr = np.array([]).reshape(0,896,608)
total_arr = np.array([]).reshape(0,480,416)
for ii,pf in enumerate(press_files):
	dt = int(os.path.basename(pf).split('.')[-2])
	curr_time = t_start+timedelta(hours=dt+xi)
	local_time = curr_time.astimezone(pytz.timezone('America/New_York'))
	np_time = np.datetime64(local_time)
	if np_time not in [x for x in list_dates]:
		continue
	#print(pf)
	press_data = PFData(pf)
	press_data.loadHeader()
	press_data.loadData()
	press_arr = press_data.getDataAsArray()
	satur_data = PFData(satur_files[ii])
	satur_data.loadHeader()
	satur_data.loadData()
	satur_arr = satur_data.getDataAsArray()
	#caculate the wtd
	satur_where = np.sum(satur_arr==1,axis=0)-1
	max_wtd = np.vectorize(depth.get)(satur_where)
	max_wtd = max_wtd.astype('float')
	m,n = satur_where.shape
	I,J = np.ogrid[:m,:n]
	sel_press = press_arr[satur_where,I,J]
	wtd = max_wtd - sel_press
	total_arr = np.vstack([total_arr,wtd[np.newaxis,...]])

#flip the daily array upside down
total_arr = total_arr[:,::-1,:]
np.save(out_name,total_arr)
