
import urllib
import requests
from datetime import datetime
from .phenolopy import calc_phenometrics as phenolopy_calc_phenometrics
from pystac_client import Client
from tqdm import tqdm
import xarray as xr
import pandas as pd
import numpy as np
import os, glob
import zipfile

url_wtss = 'https://brazildatacube.dpi.inpe.br/wtss'
url_stac = 'https://data.inpe.br/bdc/stac/v1/'

def cube_query(collection, start_date, end_date, freq, bands=None, bbox=None):
    return dict(
        collection = collection,
        bands = bands,
        start_date = start_date,
        end_date = end_date,
        freq=freq,
        bbox = bbox
    )

def get_timeseries(cube, geom):
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
        data_json = data.json()
        return data_json['result']

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
        ds = phenolopy_calc_phenometrics(da=da, peak_metric=peak_metric, base_metric=base_metric, method=method, factor=factor, thresh_sides=thresh_sides, abs_value=abs_value)
    return ds

def download_stream(file_path: str, response, chunk_size=1024*64, progress=True, offset=0, total_size=None):
    """Download request stream data to disk.

    Args:
        file_path - Absolute file path to save
        response - HTTP Response object
    """
    parent = os.path.dirname(file_path)

    if parent:
        os.makedirs(parent, exist_ok=True)

    if not total_size:
        total_size = int(response.headers.get('Content-Length', 0))

    file_name = os.path.basename(file_path)

    progress_bar = tqdm(
        desc=file_name[:30]+'... ',
        total=total_size,
        unit="B",
        unit_scale=True,
        disable=not progress,
        initial=offset
    )

    mode = 'a+b' if offset else 'wb'

    # May throw exception for read-only directory
    with response:
        with open(file_path, mode) as stream:
            for chunk in response.iter_content(chunk_size):
                stream.write(chunk)
                progress_bar.update(chunk_size)

    file_size = os.stat(file_path).st_size

    if file_size != total_size:
        os.remove(file_path)
        print(f'Download file is corrupt. Expected {total_size} bytes, got {file_size}')
     
def download(collection, start_date, end_date, bbox):
    stac = Client.open(url_stac)
    item_search = stac.search(bbox=bbox, collections=[collection],  datetime=start_date+'/'+end_date)
    if not os.path.exists('zip'):
        os.makedirs('zip')
    for item in item_search.items():
        response = requests.get(item.assets["asset"].href, stream=True)
        download_stream(os.path.basename(item.assets["asset"].href), response, total_size=item.to_dict()['assets']["asset"]["bdc:size"])

def unzip():
    for z in glob.glob("*.zip"):
        try:
            with zipfile.ZipFile(os.path.join(z), 'r') as zip_ref:
                print('Unziping '+ z)
                zip_ref.extractall('unzip')
                os.remove(z)
        except:
            print("An exception occurred")
            os.remove(z)

def cshd_img_cube(data_dir):
    list_da = []
    for path in os.listdir(data_dir):
        da = xr.open_dataarray(os.path.join(data_dir+path), engine='rasterio')
        time = path.split("_")[-2]
        dt = datetime.strptime(time, '%Y%m%d')
        dt = pd.to_datetime(dt)
        da = da.assign_coords(time = dt)
        da = da.expand_dims(dim="time")
        list_da.append(da)
    data_cube = xr.combine_by_coords(list_da)   
    return data_cube

def cshd_array(timeserie, start_date, freq):
    np_serie = np.array(timeserie, dtype=np.float32)
    dates_datetime64 = pd.date_range(pd.to_datetime(start_date, format='%Y-%m-%d'), periods=len(np_serie), freq=freq)
    data_xr = xr.DataArray(np_serie, coords = {'time': dates_datetime64})
    return data_xr

def cshd_cube(timeseries, start_date, freq):
    list_da = []
    for ts in timeseries:
        np_array = np.array(ts, dtype=np.float32)
        dates_datetime64 = pd.date_range(pd.to_datetime(start_date, format='%Y-%m-%d'), periods=len(np_array), freq=freq)
        data_xr = xr.DataArray(np_array, coords = {'time': dates_datetime64})
        list_da.append(data_xr)
    print(list_da)
    #data_cube = xr.combine_by_coords(list_da)   
    #return data_cube

    #Could not find any dimension coordinates to use to order the datasets for concatenation

def get_phenometrics(cube, geom, engine, config):

    data = get_timeseries(
        cube=cube, 
        geom=geom
    )

    data_array = cshd_array(
        timeserie=data['attributes'][0]['values'],
        start_date=cube['start_date'],
        freq=cube['freq']
    )

    ds_phenos = calc_phenometrics(
        da=data_array,
        engine=engine,
        config=config
    )

    return ds_phenos