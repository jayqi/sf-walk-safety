from flask import Flask, render_template, request, redirect
from application import app
import application.models as models

#from bokeh.embed import components

@app.route("/")
def index():
    return render_template('index.html')

defaultfilters = {
    'startDate' : '01/01/2003',
    'endDate' : '03/01/2016',
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

def get_region_radio_check(region_type):
    D = {}
    for item in ['nhood', 'tractce10', 'police_district', 'hist_police_district']:
        if item == region_type:
            D[item] = 'checked'
        else:
            D[item] = ''
    return D

regionopts = {
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

##############################################
################### THEFTS ###################
##############################################

@app.route("/thefts/")
def theft_main():
    return render_template('thefts.html')

@app.route("/thefts/mapmarkers/",methods=['GET','POST'])
def theft_markers_map():

    if request.method == 'POST':
        userfilters = get_userfilters(request.form)
        filters = userfilters
    else:
        filters = defaultfilters

    pageopts = {
        'uppercase' : 'Thefts',
        'lowercase' : 'thefts',
        'maptype' : 'Individual Incidents Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='markers',
        mapdata=models.markers_geojson(app.df_thefts,filters),
        filtersdisplay=build_filtersdisplay(filters)
        )

@app.route("/thefts/mapchoropleth/",methods=['GET','POST'])
def theft_choropleth_map():

    if request.method == 'POST':
        userfilters = get_userfilters(request.form)
        filters = userfilters
        region_type = request.form['region_type']
    else:
        filters = defaultfilters
        region_type = 'nhood'

    pageopts = {
        'uppercase' : 'Thefts',
        'lowercase' : 'thefts',
        'maptype' : 'Choropleth Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='choropleth',
        regionopts=regionopts[region_type],
        mapdata=models.choropleth_geojson(app.df_thefts,region_type,filters),
        filtersdisplay=build_filtersdisplay(filters)
        )


###############################################
################## ROBBERIES ##################
###############################################
@app.route("/robberies/")
def robbery_main():
    return render_template('robberies.html')

@app.route("/robberies/mapmarkers/",methods=['GET','POST'])
def robbery_markers_map():

    if request.method == 'POST':
        userfilters = get_userfilters(request.form)
        filters = userfilters
    else:
        filters = defaultfilters

    pageopts = {
        'uppercase' : 'Robberies',
        'lowercase' : 'robberies',
        'maptype' : 'Individual Incidents Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='markers',
        mapdata=models.markers_geojson(app.df_robberies,filters),
        filtersdisplay=build_filtersdisplay(filters)
        )

@app.route("/robberies/mapchoropleth/",methods=['GET','POST'])
def robbery_choropleth_map():

    if request.method == 'POST':
        userfilters = get_userfilters(request.form)
        filters = userfilters
        region_type = request.form['region_type']
    else:
        filters = defaultfilters
        region_type = 'nhood'

    pageopts = {
        'uppercase' : 'Robberies',
        'lowercase' : 'robberies',
        'maptype' : 'Choropleth Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='choropleth',
        regionopts=regionopts[region_type],
        mapdata=models.choropleth_geojson(app.df_robberies,region_type,filters),
        filtersdisplay=build_filtersdisplay(filters)
        )

########################################################
################## TRAFFIC COLLISIONS ##################
########################################################

@app.route("/trafficcollisions/")
def traffic_collision_main():
    return render_template('trafficcollisions.html')




###############################################
#################### OTHER ####################
###############################################

@app.route("/highlights/")
def highlights():
    #foo = models.time_of_day_plot(app.df_robberies,'Robberies')
    #plots = {'robbery-time' : foo}
    return render_template('highlights.html')

@app.route("/about/")
def aboutdata():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
