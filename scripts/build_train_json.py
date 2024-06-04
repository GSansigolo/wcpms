import os
from cshd import cube_query, get_timeseries, params_phenometrics, calc_phenometrics, cshd_array
import pandas as pd
import json

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

df = pd.read_csv(os.path.join(path_dir, "train.csv"))
timeseries_pheno_metrics = []
df = df.reset_index()  # make sure indexes pair with number of rows

for row in df.itertuples(index=True, name='Pandas'):
    print(row.longitude, row.latitude)
    ts = get_timeseries(
        cube=S2_cube, 
        geom=[dict(coordinates = [row.longitude, row.latitude])],
        cloud_filter = True
    )
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
    timeseries_pheno_metrics.append(ts['values'] + ds_phenos)

with open(os.path.join(path_dir, "test_timeseries_pheno_metrics.json"), 'w') as fp:
    json.dump(dict(timeseries_pheno_metrics = timeseries_pheno_metrics), fp)