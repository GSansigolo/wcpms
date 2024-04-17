
import urllib
import requests 

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