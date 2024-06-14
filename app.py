from flask import Flask
from flask import Blueprint, abort, request
from wcpms import params_phenometrics, cube_query, get_phenometrics, wcpms_array, calc_phenometrics

app = Flask(__name__)

bp = Blueprint('wcpms', import_name=__name__)

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
        abs_value=0.1
    )

    point = [dict(coordinates = [float(args['longitude']), float(args['latitude']) ])]
    try:
        pheno = get_phenometrics(
            cube=cube,
            geom=point,
            engine='phenolopy',
            smooth_method='savitsky',
            cloud_filter = True,
            interpolate = False,
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
'''    
@app.route("/calc_phenometrics", methods=['POST'])
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



