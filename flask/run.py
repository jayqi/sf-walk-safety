# Runs web app
from application import app

if __name__ == '__main__':
    port = 8080
    app.run('0.0.0.0', port=port)
