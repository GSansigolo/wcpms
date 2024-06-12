from cshd import params_phenometrics, cube_query, get_phenometrics

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1
)

print(config)

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2021-01-01",
    end_date="2021-12-31",
    freq='16D',
    band="NDVI"
)

print(S2_cube)

ds_phenos = get_phenometrics(
    cube=S2_cube,
    geom=[dict(coordinates = [-52.47134616677471,-13.67705998895876])],
    engine='phenolopy',
    smooth_method='savitsky',
    cloud_filter = True,
    interpolate = True,
    config=config
)

print(ds_phenos)