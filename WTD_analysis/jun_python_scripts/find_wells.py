#%%
import os
import sys
import os.path
from parflowio.pyParflowio import PFData
import gdal
from pyproj import Proj, transform
import pandas as pd
import numpy as np
#%%
# import pip
# pip.main(['install','pyproj'])
#%%
def pfread(pfbfile):
    """
    Read a pfb file and return data as an ndarray
    :param pfbfile: path to pfb file
    :return: An ndarray of ndim=3, with shape (nz, ny, nx)
    """
    if not os.path.exists(pfbfile):
        raise RuntimeError(f'{pfbfile} not found')
    pfb_data = PFData(pfbfile)
    pfb_data.loadHeader()
    pfb_data.loadData()
    arr = pfb_data.moveDataArray()
    pfb_data.close()
    assert arr.ndim == 3, 'Only 3D arrays are supported'
    return arr[:, ::-1, :]

# obs_file = sys.argv[1]
# wtd_file = sys.argv[2]
# out_file = sys.argv[3]
obs_file = 'wt_obs_US_complete'
# wtd_file = sys.argv[2]
out_file = 'icom_wells.csv'
# obs_file = 'wt_obs_US_complete'

# sel_basin = sys.argv[4]
# sel_basin = int(sel_basin)

#Read regions file to obtain projection and domain extent
# ds_reg = gdal.Open('shp/Regions.tif')
ds_reg = gdal.Open('icom_mask_final.tif')
geom_reg = ds_reg.GetGeoTransform()
arr_reg = ds_reg.ReadAsArray()

inProj = Proj(init='epsg:4326')
outProj = Proj('+proj=lcc +lat_1=30 +lat_2=60 +lat_0=40.00000762944445 +lon_0=-97 +x_0=0 +y_0=0 +a=6370000 +b=6370000 +units=m +no_defs')

# yy0,xx0 = np.where(arr_reg==sel_basin)
yy0,xx0 = np.where(arr_reg==1)
new_arr = arr_reg[min(yy0):max(yy0)+1,min(xx0):max(xx0)+1]
len_y, len_x = new_arr.shape
new_len_y = ((len_y//32)+1)*32
n1 = (new_len_y-len_y)//2
n2 = new_len_y-len_y-n1
new_len_x = ((len_x//32)+1)*32
n3 = (new_len_x-len_x)//2
n4 = new_len_x-len_x-n3

# obs_file = '/home/hoang/work/decadal_simulations/obs/Groundwater/wt_obs_US_complete'

wt_obs_arr = np.loadtxt(obs_file)

obs_lats = wt_obs_arr[:,1]
obs_lons = wt_obs_arr[:,2]
obs_wtds = wt_obs_arr[:,4]

## transform to CONUS2.0 projection
repro_lons,repro_lats = transform(inProj,outProj,obs_lons,obs_lats)

xs = (repro_lons-geom_reg[0])/geom_reg[1]
xs = xs.astype(np.int)
ys = (geom_reg[3]-repro_lats)/geom_reg[1]
ys = ys.astype(np.int)
#mask stations that out of range
xs_mask = np.ma.masked_where(np.logical_or.reduce((xs>=arr_reg.shape[1],
                                            xs<0,ys<0,
                                            ys>=arr_reg.shape[0])),xs)
ys_mask = np.ma.masked_where(np.logical_or.reduce((xs>=arr_reg.shape[1],
                                            xs<0,ys<0,
                                            ys>=arr_reg.shape[0])),ys)

# sel_idx = np.where(arr_reg[ys_mask.filled(0),xs_mask.filled(0)] == sel_basin)[0]
sel_idx = np.where(arr_reg[ys_mask.filled(0),xs_mask.filled(0)] == 1)[0]

sel_xs = xs[sel_idx]-(min(xx0)-n3)
sel_ys = ys[sel_idx]-(min(yy0)-n1)
sel_obs = obs_wtds[sel_idx]

list_coords = np.dstack([sel_xs,sel_ys])[0,:,:]
## remove duplicate
new_array = [tuple(row) for row in list_coords]
coords_uniques = np.unique(new_array,axis=0)

new_sel_xs = coords_uniques[:,0]
new_sel_ys = coords_uniques[:,1]

#Read WTD file

#wtd_file = 'extract_results/CONUS1_wtd.npy'
wtd_arr = np.load(wtd_file)
sel_mean = np.mean(wtd_arr, axis = 0)

final_xs = []
final_ys = []
final_obs = []

for jj, x in enumerate(new_sel_xs):
    print(jj)
    idxs = np.where((list_coords==coords_uniques[jj,:]).all(axis=1))[0] #get the index of mean observed wtd
    if len(idxs) > 1:
        continue
    for ii in idxs:
        obsi = sel_obs[ii]
        y = sel_ys[ii]
        x = sel_xs[ii]
        curr_best_sim_wtd = sel_mean[y, x]
        for xi in range(x - 2, x + 3):
            for yi in range(y - 2, y + 3):
                try:
                    tmp_sim_wtd = sel_mean[yi, xi]
                    if np.abs(tmp_sim_wtd - obsi) < np.abs(curr_best_sim_wtd - obsi):
                        curr_best_sim_wtd = tmp_sim_wtd
                        y = yi
                        x = xi
                except:
                    continue
        final_xs.append(x)
        final_ys.append(y)
        final_obs.append(obsi)

final_wells = pd.DataFrame()
final_wells['x'] = final_xs
final_wells['y'] = final_ys
final_wells['obs'] = final_obs

if os.path.isfile(out_file):
    os.remove(out_file)

final_wells.to_csv(out_file, index = False)



