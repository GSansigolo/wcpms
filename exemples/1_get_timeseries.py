from cshd import cube_query, get_timeseries, smooth_timeseries

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2020-01-01",
    end_date="2020-12-31",
    freq='16D',
    band="NDVI"
)

print(S2_cube)

ts = get_timeseries(
    cube=S2_cube, 
    geom=[dict(coordinates = [-52.4538803100586, -13.68668633547038])]
)

print(ts)

smooth_ts = smooth_timeseries(
    ts=ts['values'], 
    method='savitsky'
)

print(smooth_ts)