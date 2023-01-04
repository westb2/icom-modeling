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

#%%
obs_file = 'icom_wells.csv'
obs_df = pd.read_csv(obs_file)
obs_x = np.array(obs_df.x)
obs_y = np.array(obs_df.y)
obs_value = np.array(obs_df.obs)

#%%
fig, ax = plt.subplots(figsize = (8, 8))
im = ax.scatter(obs_x, obs_y, c = obs_value,
            cmap = 'RdYlBu', s = 6, 
            #alpha = 0.6, 
            norm =mpl.colors.LogNorm(1, 100))
ax.set_aspect(1)
ax.invert_yaxis()
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.8)
fig.colorbar(im, cax=cax, orientation='vertical')
fig.patch.set_facecolor('xkcd:white')
ax.set_title('Observation WTD (m)')

plt.savefig('icom_obs_wtd_map.png')
# %%
