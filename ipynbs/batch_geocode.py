import pandas as pd
import numpy as np
import time
from geopy.geocoders import GoogleV3
import pickle

def process_batch(filename):
    batch = pickle.load( open( filename+".p", "rb" ) )
    g = GoogleV3()
    out = []
    counter = 0
    for item in batch.itertuples():
        address = item[1]+' at '+item[2]+', San Francisco, CA'
        location = g.geocode(address)
        out.append((item[0],item[1],item[2],location.latitude, location.longitude))
        counter += 1
        print counter, out[-1]
        time.sleep(1)

    pickle.dump( batch, open( filename+"-out.p", "wb" ) )
