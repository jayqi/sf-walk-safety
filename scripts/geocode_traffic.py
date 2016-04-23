import os.path
import pickle
import geocoder

data_roads = pickle.load( open( "data_roads.p", "rb" ) )

filename = 'data_geocoded.txt'

if os.path.isfile(filename) :
    fr = open(filename,'r',0)
    lines = fr.readlines()
    fr.close()
    current = int(lines[-1].split('|')[0])
    current += 1
else:
    current = 0

f = open(filename,'a',0)

while current < len(data_roads):
    caseid = data_roads.index[current]
    rd1 = data_roads['PRIMARY_RD'].iloc[current]
    rd2 = data_roads['SECONDARY_RD'].iloc[current]

    g = geocoder.google(s)
    latlng = g.latlng

    newline = '|'.join([str(current),str(caseid),rd1,rd2,str(latlng[0]),str(latlng[1])])
    print newline
    f.write("%s\n" % str(newline))
    time.sleep(4)
    current += 1
