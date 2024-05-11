from cshd import cshd_img_cube, get_timeseries_cshd_cube
import os

path_dir = os.path.dirname(__file__)

S2_NDVI_cube = cshd_img_cube(
    data_dir=os.path.join(path_dir,'images/')
)

print(S2_NDVI_cube)

data = get_timeseries_cshd_cube(
    cube=S2_NDVI_cube, 
    geom=[dict(coordinates = [5792005., 9947195.])]
)

print(data)