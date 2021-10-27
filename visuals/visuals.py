import xarray as xr

path_to_pfb = "../runs/bar/icom.out.press.00000.pfb"
da = xr.open_dataarray(path_to_pfb, name="press", engine="parflow")
print(da["z"==1])
