import os

from flask import make_response, session, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from app.model.image_exchange import ImageExchange
from app.model.like import Like
from app.model.guests import GuestsCheck
from app.model.get_user_data import UserData


def init(app):
    api = Api(app)
    api.add_resource(PhotoApi, '/api/v1.0/photo/<int:phid>/')
    api.add_resource(LikeApi, '/api/v1.0/like/<int:whomid>')
    api.add_resource(LikeUncheck, '/api/v1.0/like/')
    api.add_resource(GuestApi, '/api/v1.0/guest/')


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
        if request.files:
            f = request.files['img']
            filename = secure_filename(f.filename)
            f.save(os.path.join(os.path.abspath('tmp'), filename))
            self.exchange.upload_img(os.path.join(os.path.abspath('tmp'), filename), session['id'])
            return {}, 201
        else:
            return {}, 415


class LikeUncheck(Resource):
    def __init__(self):
        self.like_model = Like()
        self.users_model = UserData()

    def get(self):
        usersid = self.like_model.uncheck_like(session['id'])
        if usersid:
            data = self.users_model.get_users(usersid)
            return {'likes': data}, 200
        else:
            return {}, 404

    def post(self):
        self.like_model.check_like(session['id'])
        return {}, 200


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


class GuestApi(Resource):
    def __init__(self):
        self.guest_model = GuestsCheck()

    def get(self):
        result = self.guest_model.get_guests(session['id'])
        if result:
            users = UserData()
            result = users.get_users(result)
            return {'guests': result}
        else:
            return {}, 404

    def post(self):
        self.guest_model.check_guest(session['id'])
        return {}, 200


class BlockApi(Resource):
    def __init__(self):
        pass

    def
