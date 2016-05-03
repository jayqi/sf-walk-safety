from flask import Flask
import os
from application.paths import *
import pandas as pd
#from flask_debugtoolbar import DebugToolbarExtension

def initialize_application():
    app = Flask('application')

    # Read data from file
    df_robberies = pd.read_pickle(os.path.join(APP_DATA, 'robbery-street.p'))
    df_thefts = pd.read_pickle(os.path.join(APP_DATA, 'theft-street.p'))
    weather = pd.read_pickle(os.path.join(APP_DATA, 'noaa-weather-downtown-sf.p'))
    df_collisions = pd.read_pickle(os.path.join(APP_DATA, 'trafficcollisions.p'))

    # Add month and year
    df_robberies['month'] = df_robberies.date.apply(lambda x: x.month)
    df_robberies['year'] = df_robberies.date.apply(lambda x: x.year)
    df_thefts['month'] = df_thefts.date.apply(lambda x: x.month)
    df_thefts['year'] = df_thefts.date.apply(lambda x: x.year)
    df_collisions['month'] = df_thefts.date.apply(lambda x: x.month)


    # Change celsius to fahrenheit
    weather.TMAX = weather.TMAX.apply(celsius2fahrenheit)
    weather.TMIN = weather.TMIN.apply(celsius2fahrenheit)

    # Join with weather
    app.df_robberies = df_robberies.merge(weather,how="inner",left_on="date",right_on="DATE")
    app.df_thefts = df_thefts.merge(weather,how="inner",left_on="date",right_on="DATE")
    app.df_collisions = df_collisions.merge(weather,how="inner",left_on="date",right_on="DATE")

    return app

def celsius2fahrenheit(T):
    return T*1.8 + 32.

app = initialize_application()

#toolbar = DebugToolbarExtension(app)

from application.controllers import *
