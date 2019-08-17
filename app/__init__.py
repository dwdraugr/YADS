from flask import Flask, session
from flask_bootstrap import Bootstrap
import app.route.app_route as route
import os

template_dir = os.path.abspath('./app/template')
print(template_dir)
application = Flask(__name__, template_folder=template_dir)
application.secret_key = 'VERYVERYSECRETKEY'
application.config['SESSION_TYPE'] = 'redis'
Bootstrap(application)
route.init(application)
# restapi.init(application)

if __name__ == '__main__':
    application.run()
