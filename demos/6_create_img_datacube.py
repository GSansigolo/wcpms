from wcpms import wcpms_img_cube
import os

path_dir = os.path.dirname(__file__)

S2_NDVI_cube = wcpms_img_cube(
    data_dir=os.path.join(path_dir,'notebooks','021037/')
)

print(S2_NDVI_cube)