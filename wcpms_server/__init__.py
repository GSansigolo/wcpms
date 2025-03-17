from .wcpms_server import cube_query, get_timeseries, list_collections, params_phenometrics, calc_phenometrics_cube, calc_phenometrics, wcpms_img_cube, wcpms_dataset, wcpms_array, get_phenometrics, calc_phenometrics_cube, get_timeseries_wcpms_dataset, smooth_timeseries, interpolate_array, generate_grid_from_geojson, create_filter_array

from flask import Flask
from werkzeug.exceptions import HTTPException, InternalServerError

def setup_app(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle exceptions."""
        if isinstance(e, HTTPException):
            return {'code': e.code, 'description': e.description}, e.code

        app.logger.exception(e)

        return {'code': InternalServerError.code,
                'description': InternalServerError.description}, InternalServerError.code

    @app.after_request
    def after_request(response):
        """Enable CORS."""
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Origin, X-Requested-With, Content-Type, Accept, Authorization')
        return response


def create_app():
    """Creates Brazil Data Cube WCPMS application from config object.

    :returns: Flask Application with config instance scope.
    """
    from .app import bp

    app = Flask(__name__)

    setup_app(app)
    
    app.register_blueprint(bp)

    return app