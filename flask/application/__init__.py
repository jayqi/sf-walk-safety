from flask import Flask
from paths import *
import pandas as pd
#from flask_debugtoolbar import DebugToolbarExtension

def initialize_application():
    app = Flask('application')
    #app.debug = True

    # Read data from file
    app.df_robberies = pd.read_pickle(os.path.join(APP_DATA, 'robbery-street.p'))
    app.df_thefts = pd.read_pickle(os.path.join(APP_DATA, 'robbery-street.p'))

    return app

app = initialize_application()

#toolbar = DebugToolbarExtension(app)

from application.controllers import *
