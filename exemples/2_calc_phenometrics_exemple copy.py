from cshd import params_phenometrics, calc_phenometrics
import xarray as xr
import numpy as np
import pandas as pd

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1
)

print(config)

np.random.seed(0)
temperature = 15 + 8 * np.random.randn(3, 2, 2)
lon = [[-99.83, -99.32], [-99.79, -99.23]]
lat = [[42.25, 42.21], [42.63, 42.59]]
time = pd.date_range("2014-09-06", periods=3)
reference_time = pd.Timestamp("2014-09-05")

da = xr.Dataset(
    data_vars=dict(
        veg_index=(["time", "x", "y"], temperature),
    ),
    coords=dict(
        time=time,
        y=(["x", "y"], lat),
        x=(["x", "y"], lon),
        spatial_ref=3577,
    )
)

print(da)

'''
---------------------------------------------------------------------------------------------
<xarray.Dataset>
Dimensions:      (time: 26, x: 1115, y: 1211)
Coordinates:
  * time         (time) datetime64[ns] 2018-01-07 2018-01-21 ... 2018-12-23
  * y            (y) float64 -2.562e+06 -2.562e+06 ... -2.574e+06 -2.574e+06
  * x            (x) float64 -1.234e+06 -1.234e+06 ... -1.222e+06 -1.222e+06
    spatial_ref  int32 3577
Data variables:
    veg_index    (time, y, x) float32 0.1249737 0.11653577 ... 0.11687457
---------------------------------------------------------------------------------------------
'''

'''
ds_phenos = calc_phenometrics(
    da=da['evi'], 
    engine='phenolopy',
    config=config
)

print(ds_phenos)
'''