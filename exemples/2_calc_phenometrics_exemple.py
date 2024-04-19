from cshd import calc_phenometrics, params_phenometrics
from datetime import datetime
import xarray as xr
import pandas as pd
import os

data_dir = os.path.dirname(__file__)

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1
)

list_da = []

for path in os.listdir(data_dir+'/images_min'):
    da = xr.open_dataarray(os.path.join(data_dir+'/images_min/'+path), engine='rasterio')
    time = path.split("_")[-2]
    dt = datetime.strptime(time, '%Y%m%d')
    dt = pd.to_datetime(dt)
    da = da.assign_coords(time = dt)
    da = da.expand_dims(dim="time")
    list_da.append(da)

evi_data_cube = xr.combine_by_coords(list_da)

ds_phenos = calc_phenometrics(
    da=evi_data_cube['band_data'],
    engine='phenolopy',
    config=config
)

print(ds_phenos)