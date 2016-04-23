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

@app.route("/thefts/kde/")
def theft_kde_map():

    filters = models.get_defaultfilters()

    pageopts = {
        'uppercase' : 'Thefts',
        'lowercase' : 'thefts',
        'maptype' : 'KDE Map',
    }

    # models.build_spatial_kde(app.df_thefts)
    temp = [
    [37.784525, -122.407664, 1.0],
    [37.774525, -122.407664, 0.9],
    [37.764525, -122.407664, 1.0],
    [37.754525, -122.407664, 0.7],
    [37.744525, -122.407664, 1.0],
    [37.734525, -122.407664, 0.5],
    [37.776593, -122.451234, 0.5],
    [37.798660, -122.416252, 0.25]
    ]
    #temp = [[-122.41967442727274, 37.75263826060606, 0.10588404972559526], [-122.42132644747475, 37.759210836363636, 0.10907519443297145], [-122.43454260909091, 37.76183986666667, 0.18899661499988335], [-122.42297846767677, 37.76315438181818, 0.15970474190592046], [-122.41802240707071, 37.764468896969696, 0.16795133503216017], [-122.41967442727274, 37.76709792727273, 0.1536246731182153], [-122.41141432626263, 37.769726957575756, 0.10120359863538037], [-122.41471836666668, 37.77235598787879, 0.14433952527258312], [-122.41802240707071, 37.7736705030303, 0.15969246464782524], [-122.4015022050505, 37.7736705030303, 0.3536416003437828], [-122.40976230606061, 37.774985018181816, 0.12033155665906509], [-122.41802240707071, 37.77629953333333, 0.24481215134723727], [-122.4015022050505, 37.77629953333333, 0.46712750055538604], [-122.40811028585858, 37.77761404848485, 0.17457344614479162], [-122.41471836666668, 37.77892856363636, 0.362631530480905], [-122.42132644747475, 37.780243078787876, 0.13429659859200932], [-122.40480624545455, 37.780243078787876, 0.2174853490609235], [-122.41306634646465, 37.78155759393939, 0.42563439098629924], [-122.4328905888889, 37.78287210909091, 0.13726082906432804], [-122.40976230606061, 37.78287210909091, 0.6495363514588601], [-122.43123856868688, 37.78418662424242, 0.1372148847677287], [-122.40811028585858, 37.78418662424242, 0.9309808802091466], [-122.42297846767677, 37.785501139393936, 0.17838447794641255], [-122.40645826565657, 37.785501139393936, 0.9657109077413274], [-122.41802240707071, 37.78681565454546, 0.27278196907052216], [-122.4015022050505, 37.78681565454546, 0.36397203828892066], [-122.41306634646465, 37.78813016969697, 0.2673271711037528], [-122.39654614444444, 37.78813016969697, 0.12474167720524593], [-122.40811028585858, 37.78944468484848, 0.5072195697422008], [-122.41967442727274, 37.7907592, 0.1703413740556572], [-122.39985018484849, 37.7907592, 0.24766704269914092], [-122.40480624545455, 37.79207371515152, 0.22929786285943024], [-122.40645826565657, 37.79338823030303, 0.21515209886016287], [-122.40811028585858, 37.79470274545454, 0.2271564575391568], [-122.40976230606061, 37.79601726060606, 0.183090402426141], [-122.41141432626263, 37.79733177575758, 0.10004868017076174], [-122.40645826565657, 37.79864629090909, 0.19607242781829748], [-122.41637038686869, 37.80653338181818, 0.1250536971080818], [-122.40976230606061, 37.8078478969697, 0.13716508608352487]]
    #out = temp

    heatdata = models.build_spatial_kde(app.df_thefts)
    out = heatdata
    out = models.drop_zeroes(heatdata)
    #print len(out)
    #out = out[::10]

    return render_template('map.html',
        pageopts=pageopts,
        maptype='heat',
        mapdata=out,
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
