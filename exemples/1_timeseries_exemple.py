from cshd import cube, get_data

S2_cube = cube(
    collection="S2-16D-2",
    start_date="2019-01-01",
    end_date="2024-12-31",
    bands=["NDVI"]
)

print(S2_cube)

data = get_data(
    cube=S2_cube, 
    geom=[dict(coordinates = [-48.419193814, -8.354332142])]
)

print(data)