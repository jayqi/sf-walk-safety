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

def applyfilters(df,filters):

    # Date (both inclusive)
    startDate = datetime.strptime(filters['startDate'],"%m/%d/%Y").date()
    endDate = datetime.strptime(filters['endDate'],"%m/%d/%Y").date()
    df = df[(df.date >= startDate) & (df.date <= endDate)]

    # Weekdays
    df = df[df['dayofweek'].apply(lambda x: x in filters['weekdays'])]

    # Time (left inclusive)
    startTime = datetime.strptime(filters['startTime'],"%H:%M").time()
    if filters['endTime'] == '24:00':
        endTime = time.max
    else:
        endTime = datetime.strptime(filters['endTime'],"%H:%M").time()
    df = df[(df.time >= startTime) & (df.time < endTime)]

    # Weather
    df = df[(df.TMAX >= float(filters['minHiTemp'])) & (df.TMAX < float(filters['maxHiTemp']))]
    df = df[(df.TMIN >= float(filters['minLoTemp'])) & (df.TMIN < float(filters['maxLoTemp']))]

    # Rain
    df = df[((df.PRCP == 0) & filters['norain']) | ((df.PRCP > 0) & filters['rained'])]

    return df

def build_colorbar(maxcount):
    delta = int(math.ceil(maxcount / 8.))
    colorbar = range(0,delta*8+1,delta)
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


# Output geojson for markers map
def markers_geojson(df,filters):

    df = df.copy()

    # Convert date and time to strings
    datetime2string(df)

    # Apply filters
    pass

    # Columns to pass
    cols = ['address', 'date', 'dayofweek', 'descript', 'time',
            'nhood', 'tractce10', 'police_district', 'hist_police_district']

    # Convert dataframe to geojson js variable
    return { 'geojson' : df_to_geojson(df, cols, lat='y', lon='x') }

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

    return {
        'geojson' : geodata,
        'colorbar' : colorbar
        }



########################################################
######################### PLOTS ########################
########################################################
def time2num(t):
    ts = t.hour * 60 + t.minute
    return ts

def scott_bw(S):
    iqr = np.subtract(*np.percentile(S, [75, 25]))
    sigma = min(S.std(),iqr)
    return 1.06*sigma*S.count()**(-0.2)

def silverman_bw(S):
    iqr = np.subtract(*np.percentile(S, [75, 25]))
    sigma = min(S.std(),iqr)
    return 0.9*sigma*S.count()**(-0.2)

class WrappedKDE:

    def __init__(self,S):
        # S is a pandas series
        self.bandwidth = silverman_bw(S)
        self.model = KernelDensity(bandwidth=self.bandwidth)
        return None

    def fit(self,data):
        self.model.fit(data.reshape(-1,1))
        return self

    def pdf(self,grid):
        grid = grid.reshape(-1,1)
        griddelta = grid[1]-grid[0]
        gridmax = grid[-1]+griddelta
        out = np.exp(self.model.score_samples(grid))
        out += np.exp(self.model.score_samples(grid-gridmax))
        out += np.exp(self.model.score_samples(grid+gridmax))
        return out

def time_of_day_plot(df,uppercase):

    df = df[df.year < 2016]

    # Grid by minute
    timegrid = np.arange(1,1440,1)

    # Initialize and fit KDE
    timekde = WrappedKDE(df.time.apply(time2num))
    timekde.fit(df.time.apply(time2num))

    # Plot histogram and KDE
    sns.distplot(df.time.apply(time2num),kde = False,norm_hist=True,bins=24)
    plt.plot(timegrid,timekde.pdf(timegrid),'-',color='#4C72B0')
    plt.axis([0,1440,0,0.0015])

    # Fix xtick labels
    hours = ['0:00','3:00','6:00','9:00','12:00','15:00','18:00','21:00','24:00']
    plt.xticks(range(0,1440,180), hours)

    # Plot labels
    plt.xlabel('Time of Day')
    plt.ylabel('Probability Density')
    plt.title('Distribution of '+uppercase+' by Time of Day (2003-2015)')
    plt.legend(['Kernel Density Estimate','Histogram'])

    script = 0
    div = 0

    return {'script' : script, 'div' : div}
