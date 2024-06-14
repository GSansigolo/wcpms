from wcpms import wcpms_img_cube, get_timeseries_wcpms_dataset
import os

path_dir = os.path.dirname(__file__)

S2_NDVI_cube = wcpms_img_cube(
    data_dir=os.path.join(path_dir,'notebooks','021037/')
)

print(S2_NDVI_cube)

data = get_timeseries_wcpms_dataset(
    cube=S2_NDVI_cube, 
    geom=[dict(coordinates = [5792005., 9947195.])]
)

print(data['values'])