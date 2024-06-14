from wcpms import cube_query, get_timeseries

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2023-01-01",
    end_date="2023-12-31",
    freq='16D',
    band="NDVI"
)

print(S2_cube)

ts = get_timeseries(
    cube=S2_cube, 
    geom=[dict(coordinates = [-53.405914,-33.707669])],
    cloud_filter = True
)

print(ts)