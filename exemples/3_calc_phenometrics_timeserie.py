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
    start_date="2019-01-01",
    end_date="2024-12-31",
    freq='16D',
    bands=["EVI"]
)

print(S2_cube)

ds_phenos = get_phenometrics(
    cube=S2_cube,
    geom=[dict(coordinates = [-48.419193814, -8.354332142])],
    engine='phenolopy',
    config=config
)

print(ds_phenos)

