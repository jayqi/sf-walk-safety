import pandas as pd
import numpy as np
import datetime as dt
import json
from shapely.geometry import shape, Point
from collections import OrderedDict

# Global counter for running a job
__counter__ = 0

###########################################
############## Open Geo Data ##############
###########################################

def open_geo_data(filename):
    path = r"../geodata/"

    with open(path+filename) as f:
        return json.load(f)

def open_neighborhood_data():
    geojson = open_geo_data('neighborhoods.geojson')

    neighborhoods = {}
    for feature in geojson['features']:
        neighborhoods[feature['properties']['nhood']] = shape(feature['geometry'])

    return neighborhoods

def open_census_tract_data():
    geojson = open_geo_data('census-tracts.geojson')

    census_tracts = {}
    for feature in geojson['features']:
        census_tracts[feature['properties']['tractce10']] = shape(feature['geometry'])

    return census_tracts

def open_police_district_data():
    geojson = open_geo_data('police-districts.geojson')

    police_districts = {}
    for feature in geojson['features']:
        police_districts[feature['properties']['district']] = shape(feature['geometry'])

    return police_districts

def open_hist_police_district_data():
    geojson = open_geo_data('hist-police-districts.geojson')

    hist_police_districts = {}
    for feature in geojson['features']:
        hist_police_districts[feature['properties']['district']] = shape(feature['geometry'])

    return hist_police_districts



###########################################
############## Open Raw Data ##############
###########################################

def open_raw_robbery_street():
    path = r"../rawdata/"
    filename = r"robbery-street.csv"

    conv = {
        'date' : lambda x: dt.datetime.strptime(x,"%Y-%m-%dT%H:%M:%S.%f").date(),
        'time' : lambda x: dt.datetime.strptime(x,"%H:%M").time()
    }

    df = pd.read_csv(path+filename,converters = conv)
    return df

def open_raw_theft_street():
    path = r"../rawdata/"
    filename = r"theft-street.csv"

    conv = {
        'date' : lambda x: dt.datetime.strptime(x,"%Y-%m-%dT%H:%M:%S.%f").date(),
        'time' : lambda x: dt.datetime.strptime(x,"%H:%M").time()
    }

    df = pd.read_csv(path+filename,converters = conv)
    return df


##########################################
############## Process Data ##############
##########################################

def xy_to_point(row):
    return Point(row['x'],row['y'])

def identify_regions(point):

    # Increment counter and print
    global __counter__
    __counter__ += 1
    print __counter__

    d_get = OrderedDict([
        ('nhood' , open_neighborhood_data()),
        ('tractce10' , open_census_tract_data()),
        ('police_district' , open_police_district_data()),
        ('hist_police_district' , open_hist_police_district_data())
        ])

    d_id = OrderedDict()


    # Iterate through all region types
    for region_type, region_dict in d_get.iteritems():

        print "...identifying " + region_type + "..."

        found = False

        # Iterate through each region polygon
        for region_id, polygon in region_dict.iteritems():

            # If found containing polygon
            if polygon.contains(point):
                found = True
                print "...found!"
                d_id[region_type] = region_id

        # If not found, put None for that region type
        if not found:
            d_id[region_type] = None



    return pd.Series([value for key, value in d_id.iteritems()],
                     index=[key for key,value in d_id.iteritems()])


def add_regions(df):
    return df.join(df.apply(xy_to_point,axis=1).apply(identify_regions))



def process_robbery_street():
    global __counter__
    __counter__ = 0
    path = r'../data/robbery-street.p'
    add_regions(open_raw_robbery_street()).to_pickle(path)
    return 0

def process_theft_street():
    global __counter__
    __counter__ = 0
    path = r'../data/theft-street.p'
    add_regions(open_raw_theft_street()).to_pickle(path)
    return 0


##########################################
########## Process Weather Data ##########
##########################################

def open_raw_weather():
    path = r"../rawdata/noaa-weather-downtown-sf.csv"
    conv = {
        'DATE' : lambda x: dt.datetime.strptime(str(x),"%Y%m%d").date(),
        }
    return pd.read_csv(path,converters = conv)

def process_weather():
    # Get data and clean up
    df = open_raw_weather()[['DATE','PRCP','TMAX','TMIN']].copy()
    df.loc[2243,'TMAX'] = np.mean([df.TMAX[2242],df.TMAX[2244]])
    df.PRCP = df.PRCP.astype(float)/10.
    df.TMAX = df.TMAX.astype(float)/10.
    df.TMIN = df.TMIN.astype(float)/10.

    # Pickle
    path = r'../data/noaa-weather-downtown-sf.p'
    df.to_pickle(path)
    return 0
