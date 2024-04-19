from cshd import calc_phenometrics, params_phenometrics
from datetime import datetime
import xarray as xr
import pandas as pd
import os, re
import glob

data_dir = os.path.dirname(__file__)

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1
)

print(config)

list_da = []

for path in os.listdir('./images'):
    da = xr.open_dataset(os.path.join(data_dir+'/images/'+path), engine='rasterio')

    time = path.split("_")[-1].split("Z")[0]
    dt = datetime.strptime(time,"%Y-%m-%dT%H:%M:%S")
    dt = pd.to_datetime(dt)

    da = da.assign_coords(time = dt)
    da = da.expand_dims(dim="time")

    list_da.append(da)

evi_data_cube = xr.combine_by_coords(list_da)

print(evi_data_cube)

'''
ds_phenos = calc_phenometrics(
    da=evi1,
    engine='phenolopy',
    config=config
)

print(ds_phenos)
'''
