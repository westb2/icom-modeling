#%%
from parflowio.pyParflowio import PFData
from pfspinup import pfio
import numpy as np

# os.chdir('/Users/junzhang/Documents/ICOM/Parflow/Transient_runs/icom_subsurface_PFBs')
# pfbin = pfio.pfread('icom_init_press_200m.pfb')

pfb_file='/Users/junzhang/Documents/ICOM/Parflow/spin_up/Files4spinup/icom_final_PME.pfb'

pfb_data = PFData(pfb_file)
pfb_data.loadHeader()
pfb_data.loadData()
data = pfb_data.getDataAsArray()

pfbin = pfio.pfread(pfb_file)
# %%
pfbdiff=data-pfbin
np.min(pfbdiff)
# %%
