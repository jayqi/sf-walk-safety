import os
from paths import *
import pandas as pd
import json


# Convert date and time to string
def datetime2string(df):
    df['date'] = df['date'].apply(lambda x: x.isoformat())
    df['time'] = df['time'].apply(lambda x: x.strftime("%H:%M"))
    pass

# http://geoffboeing.com/2015/10/exporting-python-data-geojson/
def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

# Output geojson for markers map
def markers_geojson(df):

    # Convert date and time to strings
    datetime2string(df)

    # Apply filters
    pass

    # Columns to pass
    cols = ['address', 'date', 'dayofweek', 'descript', 'time',
            'nhood', 'tractce10', 'police_district', 'hist_police_district']

    # Convert dataframe to geojson js variable
    return df_to_geojson(df, cols, lat='y', lon='x')

# Output geojson for choropleth map
def choropleth_geojson(df,region_type):

    # Apply filters
    pass

    # Counts
    counts = df[region_type].value_counts()

    # Read geojson file for region_type
    geofilename = region_type + '.geojson'
    with open(os.path.join(APP_DATA, geofilename)) as data_file:
        geodata = json.load(data_file)

    for feature in geodata['features']:
        feature['properties']['count'] = counts[feature['properties'][region_type]]

    # Convert dataframe to geojson js variable
    return geodata





####################################################################################

####################################################################################
