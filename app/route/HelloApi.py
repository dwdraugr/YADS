from flask_restful import Resource


class HelloApi(Resource):
    def get(self):
        return {'hello': 'world'}
