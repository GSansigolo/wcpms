from cshd import generate_grid_from_shapefile
import os

path_dir = os.path.dirname(__file__)

points = generate_grid_from_shapefile(
    shapefile_dir=os.path.join(path_dir, "region/POLYGON.shp"),
    grid_type='random',
    plot_size=20
)

print(points)