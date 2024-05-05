from cshd import cshd_img_cube, params_phenometrics, calc_phenometrics
import os

path_dir = os.path.dirname(__file__)

ndvi_data_cube = cshd_img_cube(
    data_dir=os.path.join(path_dir,'images/')
)

print(ndvi_data_cube)

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1,
    format='full'
)

ds_phenos = calc_phenometrics(
    da=ndvi_data_cube['band_data'],
    engine='phenolopy',
    config=config,
    start_date='2019-01-01'
)

print(ds_phenos)