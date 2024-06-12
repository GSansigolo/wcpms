from cshd import cshd_img_cube, params_phenometrics, calc_phenometrics
import os

path_dir = os.path.dirname(__file__)

S2_NDVI_cube = cshd_img_cube(
    data_dir=os.path.join(path_dir,'notebooks','021037/')
)

print(S2_NDVI_cube)

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1,
    date_format='full'
)

ds_phenos = calc_phenometrics(
    da=S2_NDVI_cube['band_data'],
    engine='phenolopy',
    config=config,
    start_date='2023-01-01'
)

print(ds_phenos)