import os
import csv
from cshd import cube_query, get_timeseries, params_phenometrics, calc_phenometrics, cshd_array, smooth_timeseries

path_dir = os.path.dirname(__file__)

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2023-01-01",
    end_date="2023-12-31",
    freq='16D',
    band="NDVI"
)

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1
)

with open(os.path.join(path_dir, "train.csv"),'r') as csvinput:
    with open(os.path.join(path_dir, "train_ts.csv"), 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append('timeseries')
        row.append('pheno_metrics')
        all.append(row)

        for row in reader:
            print(row[12], row[13])
            ts = get_timeseries(
              cube=S2_cube, 
              geom=[dict(coordinates = [row[12], row[13]])],
              cloud_filter = True
            )
            row.append(ts['values'])
            print(ts['values'])
            print('Timeseries fetched')
            ndvi_array = cshd_array(
                timeserie=ts['values'],
                start_date='2023-01-01',
                freq='16D'
            )
            ds_phenos = calc_phenometrics(
                da=ndvi_array,
                engine='phenolopy',
                config=config,
                start_date='2023-01-01'
            )
            print('Phenometrics fetched')
            row.append(ds_phenos)
            all.append(row)

        writer.writerows(all)