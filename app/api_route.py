from flask import make_response, session, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from image_exchange import ImageExchange
from like import Like


def init(app):
    api = Api(app)
    api.add_resource(PhotoApi, '/api/v1.0/photo/<int:phid>/')
    api.add_resource(LikeApi, '/api/v1.0/like/<int:whomid>')


class PhotoApi(Resource):
    def __init__(self):
        self.exchange = ImageExchange()

    def get(self, phid):
        img = self.exchange.download_img(phid)
        if img is None:
            raise ValueError('Img not found')
        response = make_response(img, 200)
        response.headers.set('Content-type', 'image')
        return response

    def post(self, phid=None):
        exchange = ImageExchange()
        if request.files:
            f = request.files['img']
            exchange.upload_img(secure_filename(f.filename), session['id'])
            return {}, 201
        else:
            return {}, 415


class LikeApi(Resource):
    def __init__(self):
        self.like_model = Like()

    def get(self, whomid):
        if 'id' in session:
            result = self.like_model.find_like(session['id'], whomid)
            if result:
                return {}, 200
            else:
                return {}, 404
        else:
            return {}, 403

    def post(self, whomid):
        if session['id'] == whomid:
            return {}, 418
        result = self.like_model.add_like(session['id'], whomid)
        if result:
            return {}, 201
        else:
            return {}, 403

    def delete(self, whomid):
        if session['id'] == whomid:
            return {}, 418
        result = self.like_model.delete_like(session['id'], whomid)
        if result:
            return {}, 204
        else:
            return {}, 404
