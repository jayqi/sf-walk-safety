from flask import Flask
#from flask_debugtoolbar import DebugToolbarExtension

app = Flask('application')
app.debug = True
#toolbar = DebugToolbarExtension(app)

from application.controllers import *
