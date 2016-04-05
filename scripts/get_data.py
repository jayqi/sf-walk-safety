import os

def download_raw_data(filename,url):
    path = '../rawdata/'
    download_data(filename,url,path)
    return 0

def download_geo_data(filename,url):
    path = '../geodata/'
    download_data(filename,url,path)
    return 0

def download_data(filename,url,path):
    # Move old file to backup
    movecommand = r'mv '+path+filename+' '+path+filename+'.bk'
    print movecommand
    print os.system(movecommand)

    # Get with curl
    curlcommand = r'curl -o ' + path+filename + ' ' + '"' + url + '"'
    print "command: ", curlcommand
    print os.system(curlcommand)

    # Save lastdownloaded file
    lastdownloadcommand = r"echo $(date) > " + path+filename + ".lastdownloaded.txt"
    print lastdownloadcommand
    print os.system(lastdownloadcommand)

    return 0

##########################################
################ Raw Data ################
##########################################

def get_full_PD_data():

    filename = r'SFPD_Incidents_-_from_1_January_2003.csv'
    url = r"https://data.sfgov.org/api/views/tmnf-yvry/rows.csv?accessType=DOWNLOAD"

    download_raw_data(filename,url)
    return 0

def get_robbery_street():

    filename = r'robbery-street.csv'
    url = r"https://data.sfgov.org/resource/cuks-n6tp.csv?%24select=descript%2C+dayofweek%2C+date%2C+time%2C+address%2C+x%2C+y&%24where=category+%3D+%27ROBBERY%27+AND+descript+like+%27%25ON+THE+STREET%25%27&%24limit=100000"

    download_raw_data(filename,url)
    return 0

def get_theft_street():

    filename = r'theft-street.csv'
    url = r"https://data.sfgov.org/resource/cuks-n6tp.csv?%24select=descript%2C+dayofweek%2C+date%2C+time%2C+address%2C+x%2C+y&%24where=category+%3D+%27LARCENY/THEFT%27+AND+%28descript+like+%27%25FROM+PERSON%25%27+OR+descript+like+%27%25PICKPOCKET%25%27+OR+descript+like+%27%25PURSESNATCH%25%27+OR+descript+%3D+%27PETTY+THEFT+OF+PROPERTY%27%29&%24limit=100000"

    download_raw_data(filename,url)
    return 0

##########################################
################ Geo Data ################
##########################################

def get_neighborhoods():

    filename = r'neighborhoods.geojson'
    url = r"https://data.sfgov.org/api/geospatial/p5b7-5n3h?method=export&format=GeoJSON"

    download_geo_data(filename,url)
    return 0

def get_census_tracts():

    filename = r'census-tracts.geojson'
    url = r"https://data.sfgov.org/api/geospatial/bwbp-wk3r?method=export&format=GeoJSON"

    download_geo_data(filename,url)
    return 0

def get_police_districts():

    filename = r'police-districts.geojson'
    url = r"https://data.sfgov.org/api/geospatial/wkhw-cjsf?method=export&format=GeoJSON"

    download_geo_data(filename,url)
    return 0

def get_historical_police_districts():

    filename = r'hist-police-districts.geojson'
    url = r"https://data.sfgov.org/api/geospatial/embj-38bg?method=export&format=GeoJSON"

    download_geo_data(filename,url)
    return 0
