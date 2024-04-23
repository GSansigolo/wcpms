from cshd import cube_query, get_timeseries

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2019-01-01",
    end_date="2024-12-31",
    freq='16D',
    bands=["EVI"]
)

print(S2_cube)

data = get_timeseries(
    cube=S2_cube, 
    geom=[dict(coordinates = [-48.419193814, -8.354332142])]
)

print(data)