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

with open(os.path.join(path_dir, "train.csv"),'r') as csvinput:
    with open(os.path.join(path_dir, "train_ts.csv"), 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('timeseries')
        all.append(row)

        for row in reader:
            print(row[12], row[13])
            ts = get_timeseries(
              cube=S2_cube, 
              geom=[dict(coordinates = [row[12], row[13]])],
              cloud_filter = True
            )
            row.append(ts['values'])
            print('Timeseries fetched')
            all.append(row)

        writer.writerows(all)