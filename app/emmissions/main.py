import pandas as pd
import geopandas as gpd
from h3 import h3
from fastapi import FastAPI

URL_HCHO = 'https://api.v2.emissions-api.org/api/v2/methane/geo.json?country=USA&begin=2021-01-01&end=2021-11-22&limit=10000000&offset=0'

bharat_hcho = gpd.read_file(URL_HCHO)

bharat_hcho['lng'] = bharat_hcho.geometry.x
bharat_hcho['lat'] = bharat_hcho.geometry.y

bharat_hcho['timestamp'] = pd.to_datetime(bharat_hcho['timestamp'])


def lat_lng_to_h3(row, h3_level=4):
    return h3.geo_to_h3(row.geometry.y, row.geometry.x, h3_level)


bharat_hcho['h3'] = bharat_hcho.apply(lat_lng_to_h3, axis=1)
bharat_hcho.set_index(['timestamp'])
app = FastAPI()

# h3_index = ''
@app.get('/api/h3_index={h3_index}')
def return_all_past_values_for_h3_index(h3_index):
    hdf = bharat_hcho[bharat_hcho['h3'] == h3_index]
    d = pd.Series(hdf['value'].values, index=hdf.timestamp).to_dict()
    return {'data':{'h3_index':h3_index, 'HCHO':d}}

@app.get('/api/fetch_latest')
def return_most_recent_value_available_for_all_h3():
    latest_h3 = bharat_hcho.loc[bharat_hcho.groupby('h3').timestamp.idxmax(),:]
    return dict([(i,[a,b]) for i, a,b in zip(latest_h3['h3'],latest_h3['value'],latest_h3['timestamp'])])

