import get_data
import process_data
import os

def check_make_directory(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return 0

# Download crime data
check_make_directory(r"../rawdata")
get_data.get_robbery_street()
get_data.get_theft_street()

# Download geo data
check_make_directory(r"../geodata")
get_data.get_neighborhoods()
get_data.get_census_tracts()
get_data.get_police_districts()
get_data.get_hist_police_districts()

# Process data
check_make_directory(r"../data")
process_data.process_robbery_street()
process_data.process_theft_street()
process_data.process_weather()
