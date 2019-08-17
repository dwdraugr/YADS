from flask_restful import Resource, Api, reqparse
from . user_info import UidGet
from . user_auth import UserLogin


def init(app):
    api = Api(app)
    api.add_resource(UidGet, '/api/v1.0/<int:uid>/', '/api/v1.0/<int:uid>/<string:data_type>')
    api.add_resource(UserLogin, '/login')


