import os
import csv
from cshd import cube_query, get_timeseries

path_dir = os.path.dirname(__file__)

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2021-01-01",
    end_date="2021-12-31",
    freq='16D',
    band="NDVI"
)

with open(os.path.join(path_dir, "train.csv"), newline='') as f:
  reader = csv.reader(f)
  for row in reader:
    ts = get_timeseries(
        cube=S2_cube, 
        geom=[dict(coordinates = [row[12], row[13]])],
        cloud_filter = True
    )
    print(ts['values'])