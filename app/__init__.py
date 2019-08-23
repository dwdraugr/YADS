from flask import Flask, session
from flask_bootstrap import Bootstrap
from flask_mail import Mail
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

application.secret_key = 'VERYVERYSECRETKEY'
application.config['SESSION_TYPE'] = 'redis'

Bootstrap(application)
route.init(application)
# restapi.init(application)

if __name__ == '__main__':
    application.run()
