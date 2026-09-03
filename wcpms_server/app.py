from flask import Flask

import json
import pyproj
import shapely.geometry
from shapely.errors import GeometryTypeError

from flask import Blueprint, abort, request
from wcpms_server import list_collections, params_phenometrics, cube_query, get_phenometrics, wcpms_get_timeseries_region

bp = Blueprint('wcpms_server', import_name=__name__)

AREA_LIMIT = 3000
"""Define area to represent 3000 ha."""

TS_LIMIT = 350
"""Define timeseries limit of 350."""

@bp.route("/phenometrics", methods=['GET'])
def get_phenometrics_timeseries():
    args = request.args.to_dict()

    if args.get('longitude') is None or args.get('latitude') is None:
        abort(400, 'Missing latitude/longitude')
    
    cube = cube_query(
        collection = args['collection'],
        start_date=f"{args['start_date']}",
        end_date=f"{args['end_date']}",
        freq=args['freq'],
        band=args['band']
    )
    
    args_cloud_filter = args.get('cloud_filter',False)
    args_interpolate  = args.get('interpolate',False)
    args_peak_metric = args.get('peak_metric','pos')
    args_base_metric = args.get('base_metric','vos')
    args_method = args.get('method','seasonal_amplitude')
    args_factor = args.get('factor',0.2)
    args_thresh_sides = args.get('thresh_sides','two_sided')
    args_abs_value = args.get('abs_value',0.1)
    
    config = params_phenometrics(
        peak_metric=args_peak_metric,
        base_metric=args_base_metric, 
        method=args_method, 
        factor=args_factor, 
        thresh_sides=args_thresh_sides, 
        abs_value=args_abs_value,
        date_format='yyyy-mm-dd'
    )

    point = [dict(coordinates = [float(args['longitude']), float(args['latitude']) ])]
    try:
        pheno = get_phenometrics(
            cube=cube,
            geom=point,
            ts_list=None,
            engine='phenolopy',
            smooth_method='None',
            cloud_filter = args_cloud_filter,
            interpolate = args_interpolate,
            config=config
        )
        cube['longitude'] = float(args['longitude'])
        cube['latitude'] = float(args['latitude'])
        return dict (
            query = cube,
            result = pheno
        )
    except:
        cube['longitude'] = float(args['longitude'])
        cube['latitude'] = float(args['latitude'])
        return dict (
            query = cube,
            result = {}
        )

@bp.route("/list_collections", methods=['GET'])
def get_list_collections():
    result = list_collections()
    return result

@bp.route("/describe", methods=['GET'])
def get_describe():
    description_json = [
        dict(Code="POS",Name="Peak of Season",Description="Highest vegetation value and time of season.",Method="Maximum value in a timeseries.",Value=True,Time=True),
        dict(Code="MOS",Name="Middle of Season",Description="Mean vegetation value and time of values in top 80 of season.",Method="Mean value and time where the left and right slope edges have increased and decreased to the 80 level of the season, respectively.",Value=True,Time=False),
        dict(Code="VOS",Name="Valley of Season",Description="Lowest vegetation value and time of season.",Method="Minimum value in a timeseries.",Value=True,Time=True),
        dict(Code="BSE",Name="Base",Description="Mean of the lowest vegetation values in season.",Method="Mean value of the lowest vegetation values to the left and right of Peak of Season.",Value=True,Time=False),
        dict(Code="SOS",Name="Start of Season",Description="Vegetation value and time at the start of season.",Method="Six methods available: 1) seasonal amplitude; 2) absolute amplitude; 3) Relative amplitude; 4) LOESS STL Trend line; 5) First value of positive slope; and 6) Median value of positive slope.",Value=True,Time=True),
        dict(Code="EOS",Name="End of season",Description="Vegetation value and time at the end of season.",Method="Six methods available: 1) seasonal amplitude; 2) absolute amplitude; 3) Relative amplitude; 4) LOESS STL Trend line; 5) First value of negative slope; and 6) Median value of negative slope.",Value=True,Time=True),
        dict(Code="LOS",Name="Length of Season",Description="Length of time (number of days) between the start and end of season.",Method="The day of year at SOS minus EOS.",Value=False,Time=True),
        dict(Code="ROI",Name="Rate of Increase",Description="The rate of vegetation 'green up' at the beginning of season.",Method="Calculated as the ratio of the difference between the left 20 and 80 levels and the corresponding time difference.",Value=True,Time=False),
        dict(Code="ROD",Name="Rate of Decrease",Description="The rate of vegetation 'green down' at the end of season.",Method="Calculated as the ratio of the difference between the right 20 and 80 levels and the corresponding time difference.",Value=True,Time=False),
        dict(Code="AOS",Name="Amplitude of Season",Description="The amplitude of vegetation values for season.",Method="The difference between the maximum value and the VOS/BSE value.",Value=True,Time=False),
        dict(Code="SIOS",Name="Short Integral of Season",Description="Represents the seasonally active vegetation and provides a larger value for herbaceous vegetation cover and smaller value for evergreen vegetation cover.",Method="Calculated using the trapezoidal rule on the total vegetation values between season start and end minus the VOS/BSE level value.",Value=True,Time=False),
        dict(Code="LIOS",Name="Long Integral of Season",Description="Represents the total productivity of vegetation when in season.",Method="Calculated using the trapezoidal rule between the total vegetation values between season start and end.",Value=True,Time=False),
        dict(Code="SIOT",Name="Short Integral of Total",Description="Represents total vegetation productivity throughout the season, and provides a larger value for herbaceous vegetation cover and smaller value for evergreen vegetation cover.",Method="Calculated using the trapezoidal rule on the total vegetation values minus the VOS/BSE level value.",Value=True,Time=False),
        dict(Code="LIOT",Name="Long Integral of Total",Description="Represents the total productivity of vegetation throughout the season.",Method="Calculated using the trapezoidal rule between the total vegetation values between season start and end.",Value=True,Time=False),
        dict(Code="NOS",Name="Number of Seasons",Description="Total number of seasons (i.e. prominent graph peaks) in timerseries.",Method="Peaks detected using scipy find_peaks and any peaks are over 3 months apart.",Value=False,Time=False)
    ]
    return dict (
        query = dict(route="describe"),
        description = description_json
    )
 
@bp.route("/phenometrics", methods=['POST'])
def get_phenometrics_region():
    args = request.args.to_dict()

    data = request.json

    if data['timeseries'] is None:
        abort(400, 'Missing Timeseries')
    
    check_timeseries(data['timeseries'])

    cube = cube_query(
        collection = data['collection'],
        start_date=f"{data['start_date']}",
        end_date=f"{data['end_date']}",
        freq=data['freq'],
        band=data['band']
    )
    
    config = params_phenometrics(
        peak_metric='pos', 
        base_metric='vos', 
        method='seasonal_amplitude', 
        factor=0.2, 
        thresh_sides='two_sided', 
        abs_value=0.1,
        date_format='yyyy-mm-dd'
    )

    try:
        pheno = get_phenometrics(
            cube=cube,
            geom=[],
            ts_list=data['timeseries'],
            engine='phenolopy',
            smooth_method='savitsky',
            cloud_filter=True,
            interpolate=True,
            config=config
        )

        return dict (
            query = cube,
            result = pheno
        )
    except:
        return dict (
            query = cube,
            result = {}
        )

@bp.route("/timeseries", methods=['POST'])
def get_timeseries_region():
    args = request.args.to_dict()

    data = request.json

    if data['geom'] is None:
        abort(400, 'Missing Geometry')

    geojson = data['geom']
    
    check_geometry(geojson)

    cube = cube_query(
        collection = data['collection'],
        start_date=f"{data['start_date']}",
        end_date=f"{data['end_date']}",
        freq=data['freq'],
        band=data['band']
    )
    
    try:
        timeseries = wcpms_get_timeseries_region(
            cube=cube,
            geojson=geojson,
            smooth_method='None'
        )

        return dict (
            query = cube,
            result = timeseries
        )
    except:
        return dict (
            query = cube,
            result = {}
        )
    
def check_geometry(query_geom):
    """Validate the geometry parameter and set a limit of area for request."""
    try:

        geom = shapely.geometry.shape(query_geom)

        # Check polygon area
        if geom.geom_type in ["Polygon", "MultiPolygon"]:
            area_ha = get_geometry_area(geom)
            
            if not area_ha:
                abort(400, "Invalid geometry.")

            if area_ha > AREA_LIMIT:
                abort(400, f'The polygon area {area_ha} must be less than {AREA_LIMIT}ha.')

        return geom

    except (json.JSONDecodeError, AttributeError, GeometryTypeError, KeyError):
        abort(400, "Invalid geometry.")

def get_geometry_area(polygon_geom):
    """Get polygon area."""
    try:
        geod = pyproj.Geod(ellps="WGS84")
        area_m2, _ = geod.geometry_area_perimeter(polygon_geom)
        area_ha = area_m2/10000
        return area_ha
    except:
        return None

def check_timeseries(timeseries):
    """Validate the timeseries parameter and set a limit of numbert per request."""
    try:

        len_ts = len(timeseries)

        if not timeseries:
            abort(400, "Invalid timeseries.")

        if len_ts > TS_LIMIT:
            abort(400, f'The number of timeseries per request ({len_ts}) must be less than ({TS_LIMIT}).')

        return len_ts

    except:
        abort(400, "Invalid timeseries.")
