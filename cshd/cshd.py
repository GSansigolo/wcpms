
import urllib
import requests
from .phenolopy import calc_phenometrics

url_wtss = 'https://brazildatacube.dpi.inpe.br/wtss'

def cube(collection, start_date, end_date, bands=None, bbox=None):
    return dict(
        collection = collection,
        bands = bands,
        start_date = start_date,
        end_date = end_date,
        bbox = bbox
    )

def get_data(cube, geom):
    dataset = []
    total_process_bar = len(geom)
    progress = 0
    for point in geom:
        progress += 1
        progress_bar = int(progress/total_process_bar*100)
        print("|"+ "=" * progress_bar+ " " * (100-progress_bar)+"| " +  str(progress_bar) + "%")
        query = dict(
            coverage=cube['collection'],
            attributes=','.join(cube['bands']),
            start_date=cube['start_date'],
            end_date=cube['end_date'],
            latitude=point['coordinates'][1],
            longitude=point['coordinates'][0],
        )
        url_suffix = '/time_series?'+urllib.parse.urlencode(query)
        print(url_wtss + url_suffix)
        data = requests.get(url_wtss + url_suffix) 
        #dataset =
        return data.json()

def params_phenometrics(peak_metric='pos', base_metric='bse', method='first_of_slope', factor=0.5, thresh_sides='two_sided', abs_value=0):
    return dict(
        peak_metric=peak_metric, 
        base_metric=base_metric, 
        method=method, 
        factor=factor, 
        thresh_sides=thresh_sides, 
        abs_value=abs_value
)

def calc_phenometrics(da, engine, config):

    peak_metric = config['peak_metric']
    base_metric = config['base_metric']
    method = config['method']
    factor = config['factor']
    thresh_sides = config['thresh_sides']
    abs_value = config['abs_value']

    if engine=='phenolopy':
        ds = calc_phenometrics(da, peak_metric, base_metric, method, factor, thresh_sides, abs_value)

    if engine=='dea':
        return print('TO DO')

    return ds