from cshd import cshd_cube
import os

path_dir = os.path.dirname(__file__)

evi_data_cube = cshd_cube(
    data_dir=os.path.join(path_dir,'images/')
)

print(evi_data_cube)