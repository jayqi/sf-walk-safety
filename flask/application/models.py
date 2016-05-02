import os
from application.paths import *
import pandas as pd
import numpy as np
from datetime import datetime, time
import math
import json

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.neighbors import KernelDensity


#######################################################
######################### MAPS ########################
#######################################################

# Convert date and time to string
def datetime2string(df):
    df['date'] = df['date'].apply(lambda x: x.isoformat())
    df['time'] = df['time'].apply(lambda x: x.strftime("%H:%M"))
    pass

def get_defaultfilters():
    return {
        'startDate' : '01/01/2013',
        'endDate' : '03/21/2016',
        'startTime' : '00:00',
        'endTime' : '24:00',
        'weekdays': [u'Monday', u'Tuesday', u'Wednesday', u'Thursday', u'Friday', u'Saturday', u'Sunday'],
        'minHiTemp' : '40',
        'maxHiTemp' : '100',
        'minLoTemp' : '35',
        'maxLoTemp' : '70',
        'norain' : True,
        'rained' : True
    }

def get_userfilters(form):
    userfilters = {}
    userfilters['startDate'], userfilters['endDate'] = map(lambda x: x.strip(),form['daterange'].split('-'))
    userfilters['startTime'] = form['startTime']
    userfilters['endTime'] = form['endTime']
    userfilters['minHiTemp'], userfilters['maxHiTemp'] = map(lambda x: x.strip(),form['hiTemp'].split(','))
    userfilters['minLoTemp'], userfilters['maxLoTemp'] = map(lambda x: x.strip(),form['loTemp'].split(','))
    userfilters['weekdays'] = form.getlist('weekdayfilter')
    if form.get("norain"):
        userfilters['norain'] = True
    else:
        userfilters['norain'] = False
    if form.get("rained"):
        userfilters['rained'] = True
    else:
        userfilters['rained'] = False
    return userfilters

def build_filtersdisplay(filters):
    filtersdisplay = {}
    filtersdisplay['startDate'] = filters['startDate']
    filtersdisplay['endDate'] = filters['endDate']
    filtersdisplay['startTime'] = filters['startTime']
    filtersdisplay['startTime'] = filters['startTime']
    filtersdisplay['endTime'] = filters['endTime']
    filtersdisplay['minHiTemp'] = filters['minHiTemp']
    filtersdisplay['maxHiTemp'] = filters['maxHiTemp']
    filtersdisplay['minLoTemp'] = filters['minLoTemp']
    filtersdisplay['maxLoTemp'] = filters['maxLoTemp']
    for weekday in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
        if weekday in filters['weekdays']:
            filtersdisplay[weekday] = 'checked'
        else:
            filtersdisplay[weekday] = ''
    if filters['norain']:
        filtersdisplay['norain'] = 'checked'
    else:
        filtersdisplay['norain'] = ''
    if filters['rained']:
        filtersdisplay['rained'] = 'checked'
    else:
        filtersdisplay['rained'] = ''
    return filtersdisplay

def applyfilters(df,filters):

    # Date (both inclusive)
    startDate = datetime.strptime(filters['startDate'],"%m/%d/%Y").date()
    endDate = datetime.strptime(filters['endDate'],"%m/%d/%Y").date()
    df = df[(df.date >= startDate) & (df.date <= endDate)].copy()

    # Weekdays
    df = df[df['dayofweek'].apply(lambda x: x in filters['weekdays'])].copy()

    # Time (left inclusive)
    startTime = datetime.strptime(filters['startTime'],"%H:%M").time()
    if filters['endTime'] == '24:00':
        endTime = time.max
    else:
        endTime = datetime.strptime(filters['endTime'],"%H:%M").time()
    df = df[(df.time >= startTime) & (df.time < endTime)].copy()

    # Weather
    df = df[(df.TMAX >= float(filters['minHiTemp'])) & (df.TMAX < float(filters['maxHiTemp']))].copy()
    df = df[(df.TMIN >= float(filters['minLoTemp'])) & (df.TMIN < float(filters['maxLoTemp']))].copy()

    # Rain
    df = df[((df.PRCP == 0) & filters['norain']) | ((df.PRCP > 0) & filters['rained'])].copy()

    return df

def build_colorbar(maxcount):
    colorbar = {}

    # Linear
    delta = int(math.ceil(maxcount / 8.))
    colorbar['lin'] = range(0,delta*8+1,delta)

    # Log
    colorbar['log'] = [int(x) for x in ([0]+(np.logspace(-3,0,8)*maxcount).tolist())]

    # Make sure they're strictly increasing
    for key,bar in colorbar.iteritems():
        for i in xrange(1,len(bar)):
            if bar[i] <= bar[i-1]+1:
                bar[i] = bar[i-1] + 2

    return colorbar

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



def get_region_radio_check(region_type):
    D = {}
    for item in ['nhood', 'tractce10', 'police_district', 'hist_police_district']:
        if item == region_type:
            D[item] = 'checked'
        else:
            D[item] = ''
    return D


def get_regionopts():
    return {
        'nhood' : {
            'key' : 'nhood',
            'radio_check' : get_region_radio_check('nhood'),
            'title' : 'Neighborhoods',
            'uppercase' : 'Neighborhood',
            'lowercase' : 'neighborhood'
        },
        'tractce10' : {
            'key' : 'tractce10',
            'radio_check' : get_region_radio_check('tractce10'),
            'title' : 'Census Tract - 2010 Census',
            'uppercase' : 'Census Tract (2010 Census)',
            'lowercase' : 'census tract'
            },
        'police_district' : {
            'key' : 'district',
            'radio_check' : get_region_radio_check('police_district'),
            'title' : 'Police Districts',
            'uppercase' : 'Police District',
            'lowercase' : 'police distrct'
        },
        'hist_police_district' : {
            'key' : 'district',
            'radio_check' : get_region_radio_check('hist_police_district'),
            'title' : 'Historical Police Districts - before July 2015',
            'uppercase' : 'Historical Police Distrct (before July 2015)',
            'lowercase' : 'police district'
        }
    }





# Output geojson for choropleth map
def choropleth_geojson(df,region_type,filters):

    df = df.copy()

    # Apply filters
    df = applyfilters(df,filters)

    # Counts
    counts = df[region_type].value_counts()

    # Read geojson file for region_type
    geofilename = region_type + '.geojson'
    with open(os.path.join(APP_DATA, geofilename)) as data_file:
        geodata = json.load(data_file)

    # Mapping from region_type to property key in the geodata
    geojson_keys = {
        'nhood' : 'nhood',
        'tractce10' : 'tractce10',
        'police_district' : 'district',
        'hist_police_district' : 'district'
    }

    maxcount = 0
    # Add count to geodata
    for feature in geodata['features']:
        if feature['properties'][geojson_keys[region_type]] in counts:
            feature['properties']['count'] = counts[feature['properties'][geojson_keys[region_type]]]
            maxcount = max(maxcount,counts[feature['properties'][geojson_keys[region_type]]])
        else:
            feature['properties']['count'] = 0

    # Create colorbar levels
    colorbar = build_colorbar(maxcount)

    return (geodata,colorbar)



# Output geojson for markers map
def markers_geojson(df,filters):

    df = df.copy()

    # Apply filters
    df = applyfilters(df,filters)

    # Convert date and time to strings
    datetime2string(df)

    # Columns to pass
    cols = ['address', 'date', 'dayofweek', 'descript', 'time',
            'nhood', 'tractce10', 'police_district', 'hist_police_district']

    # Convert dataframe to geojson js variable
    return df_to_geojson(df, cols, lat='y', lon='x')

# Output geojson for markers map
def markers_geojson_traffic(df,filters):

    df = df.copy()

    # Apply filters
    df = applyfilters(df,filters)

    # Convert date and time to strings
    datetime2string(df)

    # Columns to pass
    cols = ['date','time','dayofweek',
            'location',
            'PRIMARY_COLLISION_FACTOR',
            'PED_ACTION',
            'HIT_AND_RUN',
            'ALCOHOL_INVOLVED',
            'COUNT_PED_INJURED',
            'COUNT_PED_KILLED',
            'WEATHER',
            'ROAD_COND',
            'ROAD_SURFACE',
            'LIGHTING',
            'nhood', 'tractce10', 'police_district', 'hist_police_district']

    # Convert dataframe to geojson js variable
    return df_to_geojson(df, cols, lat='y', lon='x')

# Output geojson for markers map
def heat_listcoords(df,filters):

    df = df.copy()

    # Apply filters
    df = applyfilters(df,filters)

    # Dummy intensity
    df['intensity'] = 0.1

    return df[['y','x','intensity']].values.tolist()

########################################################
########################## KDE #########################
########################################################

def silverman_bwxy(df):
    count = df['x'].count()
    stdx = df['x'].std()
    stdy = df['y'].std()
    iqrx = np.subtract(*np.percentile(df['x'], [75, 25]))
    iqry = np.subtract(*np.percentile(df['y'], [75, 25]))
    sigma = min(stdx,stdy,iqrx,iqry)
    return 0.9*sigma*count**(-0.2)

def build_spatial_kde(df):
    spacekde = KernelDensity(bandwidth = silverman_bwxy(df[['x','y']]),metric='haversine')
    spacekde.fit(df[['x','y']])

    xmin = -122.5237517
    xmax = -122.3602017
    ymin = 37.7040012
    ymax = 37.8341382

    xv, yv = np.meshgrid(np.linspace(xmin,xmax,num=100),np.linspace(ymin,ymax,num=100))

    X_grid = np.vstack([xv.ravel(), yv.ravel()]).transpose()

    Z = np.exp(spacekde.score_samples(X_grid))

    Z = Z/Z.max()

    tol = 1e-1
    Z[abs(Z) < tol] = 0.0

    return [[point[1], point[0], point[2]] for point in zip(X_grid[:,0],X_grid[:,1],Z)]

def drop_zeroes(nparray):
    df = pd.DataFrame(nparray)
    return df[df[2]!=0.0].values.tolist()
