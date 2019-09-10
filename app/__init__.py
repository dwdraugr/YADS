from flask import Flask
from flask_bootstrap import Bootstrap
import app.api_route as rest_api
import app.route as route
import os

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": 'kostya.marinenkov@gmail.com',
    "MAIL_PASSWORD": 'sndmdyhdkugbdfze',
    "MAIL_DEFAULT_SENDER": 'kostya.marinenkov@gmail.com'
}


template_dir = os.path.abspath('./app/template')
application = Flask(__name__, template_folder=template_dir)
application.config.update(mail_settings)
application.config['RESIZE_URL'] = 'http://il-a3.21-school.ru:5000/'
application.config['RESIZE_ROOT'] = '~/py_img'

application.secret_key = 'VERYVERYSECRETKEY'
application.config['SESSION_TYPE'] = 'redis'
Bootstrap(application)


route.init(application)
rest_api.init(application)
if __name__ == '__main__':
    application.run()
