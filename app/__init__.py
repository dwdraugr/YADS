from flask import Flask

import app.route.api.route_1_0 as restapi
import app.route.app_route as route

application = Flask(__name__)
route.init(application)
restapi.init(application)

if __name__ == '__main__':
    application.run()
