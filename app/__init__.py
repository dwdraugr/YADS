from flask import Flask
from flask_moment import Moment
from flask_bootstrap import Bootstrap
import app.api_route as rest_api
import app.route as route
import os

from app import error_route

mail_settings = {
    "MAIL_SERVER": os.environ['MAIL_SERVER'],
    "MAIL_PORT": os.environ['MAIL_PORT'],
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": os.environ['MAIL_ADDR'],
    "MAIL_PASSWORD": os.environ['MAIL_PASSWD'],
    "MAIL_DEFAULT_SENDER": os.environ['MAIL_ADDR']
}

template_dir = os.path.abspath('./app/template')
application = Flask(__name__, template_folder=template_dir)
application.config.update(mail_settings)
application.config['RESIZE_URL'] = 'http://il-a3.21-school.ru:5000/'
application.config['RESIZE_ROOT'] = '~/py_img'

application.secret_key = 'VERYVERYSECRETKEY'
application.config['SESSION_TYPE'] = 'redis'
Bootstrap(application)

moment = Moment(application)

route.init(application)
rest_api.init(application)
error_route.init(application)

if __name__ == '__main__':
    application.run()
