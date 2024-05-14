
import urllib
import requests
from datetime import datetime, timedelta
from .phenolopy import calc_phenometrics as phenolopy_calc_phenometrics
from pystac_client import Client
from scipy.signal import savgol_filter
from scipy import interpolate as scipy_interpolate
from tqdm import tqdm
import xarray as xr
import pandas as pd
import numpy as np
import os, glob
import zipfile

url_wtss = 'https://brazildatacube.dpi.inpe.br/wtss'
url_stac = 'https://data.inpe.br/bdc/stac/v1/'
cloud_dict = {
    'S2-16D-2':{
        'cloud_band': 'SCL',
        'non_cloud_values': [4,5,6],
        'cloud_values': [0,1,2,3,7,8,9,10,11]
    }
}

def cube_query(collection, start_date, end_date, freq, band=None):
    """An object that contains the information associated with a collection 
    that can be downloaded or acessed.

    Args:
        collection : String containing a collection id.

        start_date String containing the start date of the associated collection. Following YYYY-MM-DD structure.

        end_date : String containing the start date of the associated collection. Following YYYY-MM-DD structure.

        freq String containing the frequency of images of the associated collection. Following (days)D structure. 

        band : Optional, string containing the band id.
    """

    return dict(
        collection = collection,
        band = band,
        start_date = start_date,
        end_date = end_date,
        freq=freq
    )

def create_filter_array(array, filter_true, filter_false):
    filter_arr = []
    nan = np.nan
    for element in array:
        if element in filter_true:
            filter_arr.append(0)
        if element in filter_false:
            filter_arr.append(1)
    return filter_arr

def get_timeseries(cube, geom, cloud_filter=None):
    for point in geom:
        query = dict(
            coverage=cube['collection'],
            attributes=cube['band'],
            start_date=cube['start_date'],
            end_date=cube['end_date'],
            latitude=point['coordinates'][1],
            longitude=point['coordinates'][0],
        )
        url_suffix = '/time_series?'+urllib.parse.urlencode(query)
        data = requests.get(url_wtss + url_suffix) 
        data_json = data.json()
        ts = np.array(data_json['result']['attributes'][0]['values'], dtype=np.float32)

        if cloud_filter:
            cloud = cloud_dict[cube['collection']]
            cloud_query = dict(
                coverage=cube['collection'],
                attributes=cloud['cloud_band'],
                start_date=cube['start_date'],
                end_date=cube['end_date'],
                latitude=point['coordinates'][1],
                longitude=point['coordinates'][0],
            )
            cloud_url_suffix = '/time_series?'+urllib.parse.urlencode(cloud_query)
            cloud_data = requests.get(url_wtss + cloud_url_suffix) 
            cloud_data_json = cloud_data.json()
            cloud_array = create_filter_array(np.array(cloud_data_json['result']['attributes'][0]['values']), cloud['cloud_values'], cloud['non_cloud_values'])
            ts = np.array(data_json['result']['attributes'][0]['values'], dtype=np.float32)
            nan = np.nan
            ts = ts*cloud_array
            ts[ts==0]=nan

        return dict(values=ts, timeline = data_json['result']['timeline'])

def smooth_timeseries(ts, method='savitsky', window_length=3, polyorder=1):

    if (method=='savitsky'):
        smooth_ts = savgol_filter(x=ts, window_length=window_length, polyorder=polyorder)

    return np.array(smooth_ts, dtype=np.float32)

def get_timeseries_cshd_dataset(cube, geom):
    band_ts = cube.sel(x=geom[0]['coordinates'][0], y=geom[0]['coordinates'][1], method='nearest')['band_data'].values
    timeline = cube.coords['time'].values
    ts = []
    for value in band_ts:
        ts.append(value[0])
    return dict(values=np.array(ts, dtype=np.float32), timeline= timeline)

def params_phenometrics(peak_metric='pos', base_metric='bse', method='first_of_slope', factor=0.5, thresh_sides='two_sided', abs_value=0, date_format=None):
    return dict(
        peak_metric=peak_metric, 
        base_metric=base_metric, 
        method=method, 
        factor=factor, 
        thresh_sides=thresh_sides, 
        abs_value=abs_value,
        date_format=date_format
    )

def calc_phenometrics(da, engine, config, start_date):
    peak_metric = config['peak_metric']
    base_metric = config['base_metric']
    method = config['method']
    factor = config['factor']
    thresh_sides = config['thresh_sides']
    abs_value = config['abs_value']
    date_format = config['date_format']

    if engine=='phenolopy':
        ds_phenos = phenolopy_calc_phenometrics(da=da, peak_metric=peak_metric, base_metric=base_metric, method=method, factor=factor, thresh_sides=thresh_sides, abs_value=abs_value)
        if date_format == 'yyyy-mm-dd': 
            sos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['sos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
            pos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['pos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
            vos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['vos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
            eos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['eos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
        else:
            sos_t = int(ds_phenos['sos_times'].values[()])
            pos_t = int(ds_phenos['pos_times'].values[()])
            vos_t = int(ds_phenos['vos_times'].values[()])
            eos_t = int(ds_phenos['eos_times'].values[()])
        return dict(
                mos_v=float(ds_phenos['mos_values'].values[()]),
                roi_v=float(ds_phenos['roi_values'].values[()]),
                rod_v=float(ds_phenos['rod_values'].values[()]),
                lios_v=float(ds_phenos['lios_values'].values[()]),
                sios_v=float(ds_phenos['sios_values'].values[()]),
                liot_va=float(ds_phenos['liot_values'].values[()]),
                siot_v=float(ds_phenos['siot_values'].values[()]),
                aos_v=float(ds_phenos['aos_values'].values[()]),
                bse_v=float(ds_phenos['bse_values'].values[()]),
                los_v=float(ds_phenos['los_values'].values[()]),
                sos_v=float(ds_phenos['sos_values'].values[()]),
                sos_t=sos_t,
                pos_v=float(ds_phenos['pos_values'].values[()]), 
                pos_t=pos_t, 
                vos_v=float(ds_phenos['vos_values'].values[()]),
                vos_t=vos_t, 
                eos_v=float(ds_phenos['eos_values'].values[()]),
                eos_t=eos_t, 
            )

def calc_phenometrics_cube(cshd_dataset, engine, config, start_date):
    peak_metric = config['peak_metric']
    base_metric = config['base_metric']
    method = config['method']
    factor = config['factor']
    thresh_sides = config['thresh_sides']
    abs_value = config['abs_value']
    date_format = config['date_format']

    if engine=='phenolopy':
        list_series = cshd_dataset.keys()
        list_pheno = []
        for ts in list_series:
            ds_phenos = phenolopy_calc_phenometrics(da=cshd_dataset[ts], peak_metric=peak_metric, base_metric=base_metric, method=method, factor=factor, thresh_sides=thresh_sides, abs_value=abs_value)
            if date_format == 'yyyy-mm-dd': 
                sos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['sos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
                pos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['pos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
                vos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['vos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
                eos_t = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(ds_phenos['eos_times'].values[()]))).strftime("%Y-%m-%dT00:00:00")
            else:
                sos_t = int(ds_phenos['sos_times'].values[()])
                pos_t = int(ds_phenos['pos_times'].values[()])
                vos_t = int(ds_phenos['vos_times'].values[()])
                eos_t = int(ds_phenos['eos_times'].values[()])
            list_pheno.append(dict(
                    mos_v=float(ds_phenos['mos_values'].values[()]),
                    roi_v=float(ds_phenos['roi_values'].values[()]),
                    rod_v=float(ds_phenos['rod_values'].values[()]),
                    lios_v=float(ds_phenos['lios_values'].values[()]),
                    sios_v=float(ds_phenos['sios_values'].values[()]),
                    liot_va=float(ds_phenos['liot_values'].values[()]),
                    siot_v=float(ds_phenos['siot_values'].values[()]),
                    aos_v=float(ds_phenos['aos_values'].values[()]),
                    bse_v=float(ds_phenos['bse_values'].values[()]),
                    los_v=float(ds_phenos['los_values'].values[()]),
                    sos_v=float(ds_phenos['sos_values'].values[()]),
                    sos_t=sos_t,
                    pos_v=float(ds_phenos['pos_values'].values[()]), 
                    pos_t=pos_t, 
                    vos_v=float(ds_phenos['vos_values'].values[()]),
                    vos_t=vos_t, 
                    eos_v=float(ds_phenos['eos_values'].values[()]),
                    eos_t=eos_t, 
                ))
            
        return list_pheno
    
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

def cshd_dataset(timeseries, start_date, freq):
    list_da = []
    for ts in timeseries:
        np_array = np.array(ts, dtype=np.float32)
        dates_datetime64 = pd.date_range(pd.to_datetime(start_date, format='%Y-%m-%d'), periods=len(np_array), freq=freq)
        data_xr = xr.DataArray(np_array, coords = {'time': dates_datetime64})
        list_da.append(data_xr)
    dict_cube = {}
    for index, element in enumerate(list_da):
        dict_cube[index] = element
    return xr.Dataset(dict_cube)

def get_phenometrics(cube, geom, engine, smooth_method, config, cloud_filter=None, interpolate=None):
            
    if len(geom)>1:
        
        ts_list = []

        for point in geom:
            ts = get_timeseries(
                cube=cube, 
                geom=[point],
                cloud_filter=cloud_filter
            )

            if (interpolate):
                ts['values'] = interpolate_array(ts['values'])

            if smooth_method=='None':
                ts_list.append(ts['values'])
            if smooth_method=='savitsky':
                ts_list.append(smooth_timeseries(ts['values'], method='savitsky'))

        data_array = cshd_dataset(
            timeseries=ts_list,
            start_date=cube['start_date'],
            freq=cube['freq']
        )

        ds_phenos = calc_phenometrics_cube(
            cshd_dataset=data_array,
            engine='phenolopy',
            config=config,
            start_date=cube['start_date'],
        )

        data = ts_list
        
    else:
    
        data = get_timeseries(
            cube=cube, 
            geom=geom,
            cloud_filter=cloud_filter
        )

        if (interpolate):
            data['values'] = interpolate_array(data['values'])

        if smooth_method=='None':
            data_array = cshd_array(
                timeserie=data['values'],
                start_date=cube['start_date'],
                freq=cube['freq']
            )

        if smooth_method=='savitsky':
            data_array = cshd_array(
                timeserie=smooth_timeseries(ts['values'], method='savitsky'),
                start_date=cube['start_date'],
                freq=cube['freq']
            )   

        ds_phenos = calc_phenometrics(
            da=data_array,
            engine=engine,
            config=config,
            start_date=cube['start_date']
        )
            
    return dict(phenometrics = ds_phenos, timeseries = data)

def interpolate_array(array):
    inds = np.arange(array.shape[0])
    good = np.where(np.isfinite(array))
    f = scipy_interpolate.interp1d(inds[good],array[good],bounds_error=False)
    return_array = np.where(np.isfinite(array),array,f(inds))
    return return_array