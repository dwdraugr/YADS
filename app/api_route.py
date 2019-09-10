from flask import make_response, send_file
from flask_restful import Resource, Api

from image_exchange import ImageExchange


def init(app):
    api = Api(app)
    api.add_resource(PhotoApi, '/api/v1.0/photo/<int:phid>/')


class PhotoApi(Resource):
    def __init__(self):
        self.exchange = ImageExchange()

    def get(self, phid):
        img = self.exchange.download_img(phid)
        if img is None:
            raise ValueError('Img not found')
        response = make_response(img)
        response.headers.set('Content-type', 'image')
        return response
