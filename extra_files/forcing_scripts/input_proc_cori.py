#%%
import pandas as pd
import numpy as np
import gdal
import netCDF4 as nc
import matplotlib as mpl
import matplotlib.pyplot as plt


from pyproj import Proj, transform
from parflowio.pyParflowio import PFData
from pfspinup import pfio
from glob import glob
from write_pfb import writeoutpfb

import datetime

#%%
dt = datetime.datetime(2003, 9, 30)
# end = datetime.datetime(2002, 10, 3)
end = datetime.datetime(2003, 10, 1)
step = datetime.timedelta(days=1)

forcing_date = []

while dt < end:
    forcing_date.append(dt.strftime('%Y-%m-%d'))
    dt += step
#%%
forcing_dir = '/global/cscratch1/sd/llc66/e3sm_scratch/cori-knl/ICoM_cmpr'
icom_locs = pd.read_csv('icom_locs.csv')
mask = pfio.pfread('icom_rmcoast3.out.mask.pfb')
out_dir = '/global/cscratch1/sd/jzhang55/ELM_running/WY2003_forcing2'

ny=416
nx=480

#reorgnized the locations to 2d array
x_loc_2d = np.zeros((nx,ny))
y_loc_2d = np.zeros((nx,ny))
x_icomloc = icom_locs['x_loc']
y_icomloc = icom_locs['y_loc']
for i in range(480):
    start_count = 416*i
    end_count = start_count+416
    x_loc_2d[i,:] = x_icomloc[start_count:end_count]
    y_loc_2d[i,:] = y_icomloc[start_count:end_count]


# force_files = glob(forcing_dir+'/*.nc')
# file_name = 'IELM_ICoM_cmpr.elm.h1.2010-08-01-00000.nc'
mask = mask[0,:,:]
mask[mask>0] = 1

#%%
# plt.imshow(mask)
# plt.colorbar()

# print(np.max(mask))
# print(np.min(mask))
#%%
# file_name = '/Volumes/GoogleDrive/My Drive/icom_forcing/test_folder/IELM_ICoM_cmpr.elm.h1.2010-08-01-00000.nc'

t = 0
t = 8736
# for file_name in enumerate(force_files):
#p_et_ave = np.zeros((8760))
ii = 0
for dd in forcing_date:
    file_name = 'case_run_ICoM_8th.elm.h1.' + dd + '-00000.nc'
    file_dir = f'{forcing_dir}/{file_name}'
    # forcing_nc=nc.Dataset(file_name[1])
    forcing_nc=nc.Dataset(file_dir)
    p_et_array = np.array(forcing_nc.variables['P_ET'])
    # plt.imshow(p_et_temp)
    # print('test1')

    p_et_icom = np.zeros((24,nx,ny))
    for i in range(nx):
        for j in range(ny):
            p_et_icom[:,i,j] = p_et_array[:,int(x_loc_2d[i,j]),int(y_loc_2d[i,j])]
            if p_et_icom[0,i,j]>1000:
                p_et_icom[:,i,j]=p_et_icom[:,(i-1),j]

    
    # print('test2')

    for tt in range(24):
        # print('test2')
        p_et_icom[tt,:,:] = p_et_icom[tt,:,:]*mask
        t_temp = str(t).zfill(5)
        # [i.zfill(8) for i in stat_list] 
        # out1 = file_name[1].split(".")[-2][0:10]
        outname = 'icom_ELM_p_et.'+t_temp+'.pfb'
        #write to pfb files
        towrite = np.zeros((10,nx,ny))
        towrite[-1,:,:] = p_et_icom[tt,:,:] * 3.6 / 0.1  #mm/s to 1/T 
        # towrite[-1,:,:] = p_et_icom[tt,:,:] / 1000 /0.1  #mm/h to 1/T 
        writeoutpfb(towrite,f'{out_dir}/{outname}')
        # print('write done')
        t = t+1


#     for tt in range(24):
#         p_et_temp = p_et_icom[tt,:,:]
#         p_et_temp[mask==0] = np.nan
#         p_et_ave_temp = np.nanmean(p_et_temp)
#         p_et_ave[ii] = p_et_ave_temp
#         ii += 1

# df = pd.DataFrame()
# df['p_et_ave_icom_elm'] = p_et_ave
# df.to_csv('p_et_icom_cropped.csv')
#%%
#check written pfbs
# elm_pfb = pfio.pfread("/Users/junzhang/Documents/ICOM/Data/ELM_Forcing/test_inputs/icom_ELM_p_et.00000.pfb")
# pme_pfb = pfio.pfread('/Users/junzhang/Documents/ICOM/Parflow/ELM_forcing/forcing_test/PMEtest.00000.pfb')

# %%
