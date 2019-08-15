from flask_restful import Resource, Api
from . user_info import UidGet


def init(app):
    api = Api(app)
    api.add_resource(UidGet, '/api/v1.0/<int:uid>/', '/api/v1.0/<int:uid>/<string:data_type>')


