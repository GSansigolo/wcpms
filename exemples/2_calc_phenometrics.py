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
temperature = 15 + 8 * np.random.randn(2, 2, 3)
lon = [[-99.83, -99.32], [-99.79, -99.23]]
lat = [[42.25, 42.21], [42.63, 42.59]]
time = pd.date_range("2014-09-06", periods=3)
reference_time = pd.Timestamp("2014-09-05")

da = xr.DataArray(
    data=temperature,
    dims=["x", "y", "time"],
    coords=dict(
        lon=(["x", "y"], lon),
        lat=(["x", "y"], lat),
        time=time,
        reference_time=reference_time,
    ),
    attrs=dict(
        description="Ambient temperature.",
        units="degC",
    ),
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
<xarray.DataArray (x: 2, y: 2, time: 3)> Size: 96B
array([[[29.11241877, 18.20125767, 22.82990387],
        [32.92714559, 29.94046392,  7.18177696]],

       [[22.60070734, 13.78914233, 14.17424919],
        [18.28478802, 16.15234857, 26.63418806]]])
Coordinates:
    lon             (x, y) float64 32B -99.83 -99.32 -99.79 -99.23
    lat             (x, y) float64 32B 42.25 42.21 42.63 42.59
  * time            (time) datetime64[ns] 24B 2014-09-06 2014-09-07 2014-09-08
    reference_time  datetime64[ns] 8B 2014-09-05
Dimensions without coordinates: x, y
Attributes:
    description:  Ambient temperature.
    units:        degC
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