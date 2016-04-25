from flask import Flask, render_template, request, redirect
from application import app
import application.models as models

#from bokeh.embed import components

@app.route("/")
def index():
    return render_template('index.html')


##############################################
################### THEFTS ###################
##############################################

@app.route("/thefts/")
def theft_main():
    return render_template('thefts.html')

@app.route("/thefts/mapchoropleth/",methods=['GET','POST'])
def theft_choropleth_map():

    if request.method == 'POST':
        userfilters = models.get_userfilters(request.form)
        filters = userfilters
        region_type = request.form['region_type']
    else:
        filters = models.get_defaultfilters()
        region_type = 'nhood'

    pageopts = {
        'uppercase' : 'Thefts',
        'lowercase' : 'thefts',
        'maptype' : 'Choropleth Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='choropleth',
        regionopts=models.get_regionopts()[region_type],
        mapdata=models.choropleth_geojson(app.df_thefts,region_type,filters),
        filtersdisplay=models.build_filtersdisplay(filters)
        )

@app.route("/thefts/mapmarkers/",methods=['GET','POST'])
def theft_markers_map():

    if request.method == 'POST':
        userfilters = models.get_userfilters(request.form)
        filters = userfilters
    else:
        filters = models.get_defaultfilters()

    pageopts = {
        'uppercase' : 'Thefts',
        'lowercase' : 'thefts',
        'maptype' : 'Individual Incidents Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='markers',
        mapdata=models.markers_geojson(app.df_thefts,filters),
        filtersdisplay=models.build_filtersdisplay(filters)
        )

@app.route("/thefts/mapheat/",methods=['GET','POST'])
def thefts_heat_map():

    if request.method == 'POST':
        userfilters = models.get_userfilters(request.form)
        filters = userfilters
    else:
        filters = models.get_defaultfilters()

    pageopts = {
        'uppercase' : 'Thefts',
        'lowercase' : 'thefts',
        'maptype' : 'Heat Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='heat',
        mapdata=models.heat_listcoords(app.df_thefts,filters),
        filtersdisplay=models.build_filtersdisplay(filters)
        )

@app.route("/thefts/mapkde/")
def thefts_kde_map():

    filters = models.get_defaultfilters()

    pageopts = {
        'uppercase' : 'Thefts',
        'lowercase' : 'thefts',
        'maptype' : 'Kernel Density Estimate',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='kde',
        filtersdisplay=models.build_filtersdisplay(filters)
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
        userfilters = models.get_userfilters(request.form)
        filters = userfilters
    else:
        filters = models.get_defaultfilters()

    pageopts = {
        'uppercase' : 'Robberies',
        'lowercase' : 'robberies',
        'maptype' : 'Individual Incidents Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='markers',
        mapdata=models.markers_geojson(app.df_robberies,filters),
        filtersdisplay=models.build_filtersdisplay(filters)
        )

@app.route("/robberies/mapchoropleth/",methods=['GET','POST'])
def robbery_choropleth_map():

    if request.method == 'POST':
        userfilters = models.get_userfilters(request.form)
        filters = userfilters
        region_type = request.form['region_type']
    else:
        filters = models.get_defaultfilters()
        region_type = 'nhood'

    pageopts = {
        'uppercase' : 'Robberies',
        'lowercase' : 'robberies',
        'maptype' : 'Choropleth Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='choropleth',
        regionopts=models.get_regionopts()[region_type],
        mapdata=models.choropleth_geojson(app.df_robberies,region_type,filters),
        filtersdisplay=models.build_filtersdisplay(filters)
        )

@app.route("/robberies/mapheat/",methods=['GET','POST'])
def robberies_heat_map():

    if request.method == 'POST':
        userfilters = models.get_userfilters(request.form)
        filters = userfilters
    else:
        filters = models.get_defaultfilters()

    pageopts = {
        'uppercase' : 'Robberies',
        'lowercase' : 'robberies',
        'maptype' : 'Heat Map',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='heat',
        mapdata=models.heat_listcoords(app.df_robberies,filters),
        filtersdisplay=models.build_filtersdisplay(filters)
        )

@app.route("/robberies/mapkde/")
def robberies_kde_map():

    filters = models.get_defaultfilters()

    pageopts = {
        'uppercase' : 'Robberies',
        'lowercase' : 'robberies',
        'maptype' : 'Kernel Density Estimate',
    }

    return render_template('map.html',
        pageopts=pageopts,
        maptype='kde',
        filtersdisplay=models.build_filtersdisplay(filters)
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
