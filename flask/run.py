# Runs web app
from application import app
from flask_frozen import Freezer
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
         freezer = Freezer(app)
         freezer.freeze()
    else:
        port = 8080
        app.run('0.0.0.0', port=port)
