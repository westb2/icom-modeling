#%%
import numpy as np
import pandas as pd
import matplotlib as mpl
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly as py
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from pfspinup import pfio
import glob


#%%
force_dir = '/global/cscratch1/sd/jzhang55/ELM_running/WY2003_forcing'
# force_dir = '/glade/scratch/junzhang55/icom/ELM_P_ET'
mask = pfio.pfread('icom_rmcoast3.out.mask.pfb')
masktop = mask[-1,:,:]
masktop[masktop>0]=1
pet_ave = np.zeros((8760))

ny=416
nx=480
pet_spatial = np.zeros((nx,ny))

for t in range(8760):
    t_temp = str(t).zfill(5)
    filename = 'icom_ELM_p_et.'+t_temp+'.pfb'
    
    pfbin = pfio.pfread(f'{force_dir}/{filename}')
    pet = pfbin[-1,:,:]*0.1
    pet[masktop==0]=np.nan
    pet_ave[t] = np.nanmean(pet)

    if t == 0:
        pet_spatial = pet
    else:
        pet_spatial = pet_spatial + pet

np.save('pet_spatial.npy',pet_spatial)

df = pd.DataFrame()
df['elm_p_et'] = pet_ave
df.to_csv('elm_p_et.csv')

fig, axs = plt.subplots(1,2, figsize = (20,10))
ax0 = axs[0]

im0 = ax0.imshow(np.flipud(pet_spatial))
# ax0.colorbar()
ax0.set_title('Accumulated P-ET WY2003(m)')
divider = make_axes_locatable(ax0)
cax = divider.append_axes('right', size='5%', pad=0.8)
fig.colorbar(im0, cax=cax, orientation='vertical')
# np.save('pet_ave',pet_ave)
ax1 = axs[1]
ax1.plot(pet_ave)
ax1.set_ylabel('P-ET(m/h)')
fig.savefig('pet_ave.png')

#%%
# pet_elm = np.load('pet_ave.npy')


# %%
# pme_long = pfio.pfread('icom_rm_coast_PME3.pfb')
# pme_annual = np.zeros((ny,nx))
# pme_annual = pme_long[-1,:,:]*0.1*8760

# plt.imshow(np.flipud(pme_annual))
# plt.colorbar()
