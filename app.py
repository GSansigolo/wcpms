from flask import Flask
from flask import Blueprint, abort, request
from wcpms_server import list_collections, params_phenometrics, cube_query, get_phenometrics, wcpms_array, calc_phenometrics

app = Flask(__name__)

bp = Blueprint('wcpms_server', import_name=__name__)

@app.route("/phenometrics", methods=['GET'])
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
    
    config = params_phenometrics(
        peak_metric='pos', 
        base_metric='vos', 
        method='seasonal_amplitude', 
        factor=0.2, 
        thresh_sides='two_sided', 
        abs_value=0.1,
        date_format='yyyy-mm-dd'
    )

    point = [dict(coordinates = [float(args['longitude']), float(args['latitude']) ])]
    try:
        pheno = get_phenometrics(
            cube=cube,
            geom=point,
            engine='phenolopy',
            smooth_method='savitsky',
            cloud_filter = True,
            interpolate = True,
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

@app.route("/list_collections", methods=['GET'])
def get_list_collections():
    result = list_collections()
    return result

@app.route("/describe", methods=['GET'])
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
    return description_json

'''    
@app.route("/phenometrics_region", methods=['POST'])
def calc_phenometrics_timeseries():
    args = request.json

    if args['timeserie'] is None:
        abort(400, 'Missing timeserie')

    array = wcpms_array(
        timeserie=args['timeserie'],
        start_date=f"{args['start_date']}",
        freq=args['freq'],
    )

    config = params_phenometrics(
        peak_metric='pos', 
        base_metric='vos', 
        method='seasonal_amplitude', 
        factor=0.2, 
        thresh_sides='two_sided', 
        abs_value=0.1
    )

    return calc_phenometrics(
        da=array,
        engine='phenolopy',
        config=config,
        start_date=f"{args['start_date']}",
    )
'''



