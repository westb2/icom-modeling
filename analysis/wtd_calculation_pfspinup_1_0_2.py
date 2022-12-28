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
from pfspinup.pfmetadata import PFMetadata
from pfspinup.common import calculate_surface_storage, calculate_subsurface_storage, calculate_water_table_depth, \
    calculate_evapotranspiration, calculate_overland_flow_grid

# sim_year = sys.argv[1]
# sim_year = int(sim_year)

sim_year = 2003
indir = sys.argv[1]
#indir = 'USGS'
#out_name = indir + '_wtd'
out_name = sys.argv[2]
# indir = sys.argv[2]
# if indir[-1] == '/':
#         indir = indir[:-1]
RUN_DIR = sys.argv[1]
RUN_NAME = sys.argv[2]
out_name = indir + '_wtd'

# RUN_DIR = '../pfspinup/data/example_run'
# RUN_NAME = 'LW_CLM_Ex4'

metadata = PFMetadata(f'{RUN_DIR}/{RUN_NAME}.out.pfmetadata')

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
# Time-variant values
# ------------------------------------------
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

# specify the daily array

wtd = np.zeros((nt, ny, nx))
for i, (pressure_file, saturation_file) in enumerate(zip(pressure_files, saturation_files)):
    pressure = metadata.pfb_data(pressure_file)
    saturation = metadata.pfb_data(saturation_file)

    wtd[i, ...] = calculate_water_table_depth(pressure, saturation, dz)

#flip the daily array upside down
wtd = wtd[:,::-1,:]


np.save(out_name,wtd)
