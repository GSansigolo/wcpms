from cshd import calc_phenometrics
import os
import xarray as xr

script_dir = os.path.dirname(__file__)

evi1 = xr.open_dataset(os.path.join(script_dir, "S2-16D_V2_028015_20220101_EVI.tiff"), engine='rasterio')

print(evi1)

ds_phenos = calc_phenometrics(
    da=evi1, 
    engine='phenolopy'
)

print(ds_phenos)