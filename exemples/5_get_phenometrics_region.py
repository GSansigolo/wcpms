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
    start_date="2020-01-01",
    end_date="2020-12-31",
    freq='16D',
    band="NDVI"
)

print(S2_cube)

ds_phenos = get_phenometrics(
    cube=S2_cube,
    geom=[
        dict(coordinates = [-52.4538803100586,-13.68668633547038]),
        dict(coordinates = [-52.443585438179454,-13.700154950633532]),
        dict(coordinates = [-52.46336495730327,-13.686163383245912]),
        dict(coordinates = [-52.46492649828653,-13.69830069437991]),
        dict(coordinates = [-52.4822769536588,-13.708751765727385]),
        dict(coordinates = [-52.47134616677471,-13.67705998895876]),
        dict(coordinates = [-52.441503383534496,-13.71279721691208]),
        dict(coordinates = [-52.45364870229528,-13.707571829339443]),
    ],
    engine='phenolopy',
    smooth_method='savitsky',
    cloud_filter=True,
    interpolate=True,
    config=config
)

print(ds_phenos)