from cshd import generate_grid_from_shapefile, params_phenometrics, cube_query, get_phenometrics
from shapely.geometry import shape
import fiona
import os

path_dir = os.path.dirname(__file__)

with fiona.open(os.path.join(path_dir, "notebooks", "region/POLYGON.shp")) as shapefile:
    for record in shapefile:
        geometry = shape(record['geometry'])

points = generate_grid_from_shapefile(
    shapefile_dir=os.path.join(path_dir, "notebooks", "region/POLYGON.shp"),
    grid_type='systematic',
    distance=0.18
)

points_dict_list = []
for p in points:
    points_dict_list.append(dict(coordinates = p))

print(points_dict_list)

config = params_phenometrics(
    peak_metric='pos', 
    base_metric='vos', 
    method='seasonal_amplitude', 
    factor=0.2, 
    thresh_sides='two_sided', 
    abs_value=0.1,
    date_format='yyyy-mm-dd'
)

print(config)

S2_cube = cube_query(
    collection="S2-16D-2",
    start_date="2020-01-01",
    end_date="2020-12-31",
    freq='16D',
    band="NDVI"
)

print(S2_cube)

s_phenos = get_phenometrics(
    cube=S2_cube,
    geom=points_dict_list,
    engine='phenolopy',
    smooth_method='savitsky',
    cloud_filter=True,
    interpolate=True,
    config=config
)

print(s_phenos)