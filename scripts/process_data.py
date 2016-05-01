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

def open_raw_trafficcollisions():
    path = r"../rawdata/"
    filename = r"traffic-CollisionRecords.csv"

    df = pd.read_csv(path+filename)

    return df

def open_trafficcollisions_geocoded():
    path = r"../scripts/"
    filename = r"data_geocoded.txt"

    geocode = pd.read_csv(path+filename,
            sep='|',
            header=None,
            names=['CASE_ID','PRIMARY_RD','SECONDARY_RD','y','x']
        )

    return geocode

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

##########################################
########## Process Traffic Data ##########
##########################################

def join_geocode(df):

    # Read geocode latlong
    geocode = pd.read_csv('../scripts/data_geocoded.txt',sep='|',header=None,names=['CASE_ID','PRIMARY_RD','SECONDARY_RD','y','x'])

    # Join data with geocoded lat/long
    geocode = open_trafficcollisions_geocoded()
    df.reset_index(inplace=True)
    df = df.merge(geocode[['CASE_ID','x','y']],how="inner",left_on="CASE_ID",right_on="CASE_ID")

    return df

def clean_trafficcollisions(df):

    # Convert date and time to datetime types
    df['COLLISION_DATE'] = df['COLLISION_DATE'].apply(lambda x: dt.datetime.strptime(str(x).zfill(8),"%Y%m%d").date())
    df['COLLISION_TIME'] = df['COLLISION_TIME'].apply(lambda x: dt.datetime.strptime(str(x % 2400).zfill(4),"%H%M").time())

    # Merge weather columns
    df['WEATHER'] = df[['WEATHER_1','WEATHER_2']].apply(lambda row : merge_weather(row[0],row[1]), axis=1)

    # Decode day of week
    Day_of_Week_Decode = {
            1 : 'Monday',
            2 : 'Tuesday',
            3 : 'Wednesday',
            4 : 'Thursday',
            5 : 'Friday',
            6 : 'Saturday',
            7 : 'Sunday'
        }
    df['DAY_OF_WEEK'] = df['DAY_OF_WEEK'].apply(lambda x : Day_of_Week_Decode[x])

    # Merge detailed location info
    df['location'] = df[['PRIMARY_RD','SECONDARY_RD','INTERSECTION','DISTANCE','DIRECTION']].apply(merge_location,axis=1)

    # Decode primary collision factor
    PCF_Decode = {
            '01' : "Driving or bicycling under the influence of alcohol or drug",
            '02' : "Impeding traffic",
            '03' : "Unsafe speed",
            '04' : "Following too closely",
            '05' : "Wrong side of road",
            '06' : "Improper passing",
            '07' : "Unsafe lane change",
            '08' : "Improper turning",
            '09' : "Automobile right of way",
            '10': "Pedestrian right of way",
            '11': "Pedestrian violation",
            '12': "Traffic signals and signs",
            '13': "Hazardous parking",
            '14': "Lights",
            '15': "Brakes",
            '16': "Other equipment",
            '17': "Other hazardous violation",
            '18': "Other than driver (or pedestrian)",
            '19': "Unknown",
            '20': "Unknown",
            '21': "Unsafe starting or backing",
            '22': "Other improper driving",
            '23': 'Pedestrian or "other" under the influence of alcohol or drug',
            '24': "Fell asleep",
            '00': "Unknown",
            '-' : "Unknown"
        }
    df['PRIMARY_COLLISION_FACTOR'] = df['PCF_VIOL_CATEGORY'].apply(lambda x: PCF_Decode[x.strip()])

    # Decode hit and run
    Hit_and_Run_Decode = {
            'N' : "No",
            'F' : 'Hit and run (felony)',
            'M' : 'Hit and run (misdemeanor)'
        }
    df['HIT_AND_RUN'] = df['HIT_AND_RUN'].apply(lambda x: Hit_and_Run_Decode[x.strip()])

    # Decode pedestrian action
    Ped_Action_Decode = {
            'B' : 'Crossing, in crosswalk at intersection',
            'C' : 'Crossing, in crosswalk not at intersection',
            'D' : 'Crossing, not in crosswalk',
            'E' : 'In road, including shoulder',
            'F' : 'Not in road',
            'G' : 'Approaching or leaving school bus',
            '-' : 'Unknown'
        }
    df['PED_ACTION'] = df['PED_ACTION'].apply(lambda x: Ped_Action_Decode[x.strip()])

    # Decode road surface
    Road_Surface_Decode = {
            'A' : 'Dry',
            'B' : 'Wet',
            'C' : 'Snowy or Icy',
            'D' : 'Slippery (Muddy, Oily, etc.)',
            '-' : 'Unknown'
        }
    df['ROAD_SURFACE'] = df['ROAD_SURFACE'].apply(lambda x: Road_Surface_Decode[x.strip()])

    # Merge road conditions
    df['ROAD_COND'] = df[['ROAD_COND_1','ROAD_COND_2']].apply(merge_road_conditions,axis=1)

    # Lighting conditions
    Lighting_Decode = {
            'A' : 'Daylight',
            'B' : 'Dusk or Dawn',
            'C' : 'Dark - Street lights',
            'D' : 'Dark - No street lights',
            'E' : 'Dark - Street lights not functioning',
            '-' : 'Unknown'
        }
    df['LIGHTING'] = df['LIGHTING'].apply(lambda x: Lighting_Decode[x])

    # Alcohol involved
    df[df['ALCOHOL_INVOLVED'] == 'Y'] = True
    df['ALCOHOL_INVOLVED'].fillna(value=False,inplace=True)

    # Pedestrians involved
    df['COUNT_PED_KILLED'] = df['COUNT_PED_KILLED'].apply(int)

    # Filter columns
    keepcols = [
            'ACCIDENT_YEAR',
            'COLLISION_DATE',
            'COLLISION_TIME',
            'DAY_OF_WEEK',
            'location',
            'WEATHER',
            'PRIMARY_COLLISION_FACTOR',
            'HIT_AND_RUN',
            'PED_ACTION',
            'ROAD_SURFACE',
            'ROAD_COND',
            'LIGHTING',
            'ALCOHOL_INVOLVED',
            'COUNT_PED_KILLED',
            'COUNT_PED_INJURED',
            'y',
            'x'
        ]
    df = df[keepcols]

    # Rename columns
    df.rename(columns={
            'ACCIDENT_YEAR': 'year',
            'COLLISION_DATE': 'date',
            'COLLISION_TIME' : 'time',
            'DAY_OF_WEEK' : 'dayofweek'
        },inplace=True)

    return df

def merge_weather(w1,w2):

    Weather_Decode = {
        'A' : 'Clear',
        'B' : 'Cloudy',
        'C' : 'Raining',
        'D' : 'Snowing',
        'E' : 'Fog',
        'F' : 'Other',
        'G' : 'Wind',
        '-' : None
    }

    out = ''

    if Weather_Decode[w1]:

        out = Weather_Decode[w1]

        if Weather_Decode[w2]:
            out = ', '.join([out, Weather_Decode[w2]])

    elif Weather_Decode[w2]:
        out = Weather_Decode[w2]

    return out


def merge_location(S):

    Direction_Decode = {
        'N' : 'north',
        'W' : 'west',
        'E' : 'east',
        'S' : 'south'
    }

    loc = ' and '.join([S['PRIMARY_RD'].strip(), S['SECONDARY_RD'].strip()])

    if S['INTERSECTION'] == 'Y':
        loc = ', '.join([loc, 'at intersection'])
    elif not pd.isnull(S['DISTANCE']) and not pd.isnull(S['DIRECTION']):
        direction = ' ft '.join([str(S['DISTANCE']), Direction_Decode[S['DIRECTION']] ])
        loc = ', '.join([loc, direction])

    return loc

def merge_road_conditions(S):

    Road_Cond_Decode = {
        'A' : 'Holes or deep ruts',
        'B' : 'Loose material on roadway',
        'C' : 'Obstruction on roadway',
        'D' : 'Construction or repair zone',
        'E' : 'Reduced roadway width',
        'F' : 'Flooded',
        'G' : 'Other',
        'H' : 'No unusual condition',
        '-' : 'Unknown'
    }

    out = Road_Cond_Decode[S['ROAD_COND_1']]

    if S['ROAD_COND_2'] != '-':
        out = ', '.join([out, Road_Cond_Decode[S['ROAD_COND_2']]])

    return out






def process_traffic_collisions():

    # Read data
    df = open_raw_trafficcollisions()

    # Drop non-pedestrian accidents
    df = df[pd.notnull(df['PEDESTRIAN_ACCIDENT'])].copy()
    df = df[df['PED_ACTION'] != 'A'].copy()

    # Add geocoded lat/long
    df = join_geocode(df)

    # Clean
    df = clean_trafficcollisions(df)

    global __counter__
    __counter__ = 0

    path = r'../data/trafficcollisions.p'
    add_regions(df).to_pickle(path)
    return 0
