from cshd import cshd_img_cube
import os

path_dir = os.path.dirname(__file__)

ndvi_data_cube = cshd_img_cube(
    data_dir=os.path.join(path_dir,'images/')
)

print(ndvi_data_cube)