from cshd import cube, get_data

S2_cube = cube(
    "S2-16D-2",
    "2019-01-01",
    "2024-12-31",
    ["NDVI"]
)

print(S2_cube)

data = get_data(
    S2_cube, 
    [dict(coordinates = [-48.419193814, -8.354332142])]
)

print(data)