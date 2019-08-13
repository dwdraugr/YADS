from flask_restful import Resource, Api
from . HelloApi import HelloApi
from . UidAPI import UidAll


def init(app):
    api = Api(app)
    api.add_resource(UidAll, '/api/v1.0/<int:uid>/', '/api/v1.0/<int:uid>/<string:data_type>')


