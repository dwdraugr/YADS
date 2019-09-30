import os
from flask import make_response, session, request
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from app.model.image_exchange import ImageExchange
from app.model.like import Like
from app.model.guests import GuestsCheck
from app.model.get_user_data import UserData
from app.model.block import Block
from app.model.online import Online
from app.model.messages import Messages


def init(app):
    api = Api(app)
    api.add_resource(PhotoApi, '/api/v1.0/photo/<int:phid>/')
    api.add_resource(LikeApi, '/api/v1.0/like/<int:whomid>')
    api.add_resource(LikeUncheckApi, '/api/v1.0/like/')
    api.add_resource(GuestApi, '/api/v1.0/guest/')
    api.add_resource(BlockApi, '/api/v1.0/block/<int:whomid>')
    api.add_resource(OnlineAPi, '/api/v1.0/online/<int:uid>')
    api.add_resource(MessageApi, '/api/v1.0/message/<int:you_id>')
    api.add_resource(MessageNonCheckApi, '/api/v1.0/message_non_check/<int:you_id>')
    api.add_resource(MessageNumApi, '/api/v1.0/message/')
    api.add_resource(LastMessageApi, '/api/v1.0/last_message/<int:you_id>')


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
            self.exchange.upload_img(
                os.path.join(os.path.abspath('tmp'), filename), session['id'])
            return {}, 201
        else:
            return {}, 203

    def delete(self, phid):
        self.exchange.delete_image(session['id'], phid)
        return {}, 204


class LikeUncheckApi(Resource):
    def __init__(self):
        self.like_model = Like()
        self.users_model = UserData()

    def get(self):
        usersid = self.like_model.uncheck_like(session['id'])
        if usersid:
            data = self.users_model.get_users(usersid)
            return {'likes': data}, 200
        else:
            return {}, 204

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
                return {}, 204
        else:
            return {}, 203

    def post(self, whomid):
        if session['id'] == whomid:
            return {}, 418
        result = self.like_model.add_like(session['id'], whomid)
        if result:
            return {}, 201
        else:
            return {}, 203

    def delete(self, whomid):
        if session['id'] == whomid:
            return {}, 418
        result = self.like_model.delete_like(session['id'], whomid)
        if result:
            return {}, 200
        else:
            return {}, 204


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
            return {}, 204

    def post(self):
        self.guest_model.check_guest(session['id'])
        return {}, 200


class BlockApi(Resource):
    def __init__(self):
        self.block_model = Block()

    def get(self, whomid):
        result = self.block_model.get_block(session['id'], whomid)
        if result:
            return {}, 200
        else:
            return {}, 204

    def put(self, whomid):
        result = self.block_model.block_user(session['id'], whomid)
        if result:
            return {}, 200
        else:
            return {}, 208

    def delete(self, whomid):
        result = self.block_model.unblock_user(session['id'], whomid)
        if result:
            return {}, 204
        else:
            return {}, 204


class OnlineAPi(Resource):
    def __init__(self):
        self.online_model = Online()

    def get(self, uid):
        result = self.online_model.get_online(uid)
        if result:
            return {'online': str(result)}, 200
        else:
            return {'online': 'Not found'}, 204


class MessageNumApi(Resource):
    def __init__(self):
        self.message_model = Messages()

    def get(self):
        result = self.message_model.check_all_new_message(session['id'])
        if result:
            return {'num_message': result[0]['count']}, 200
        else:
            return {}, 204


class LastMessageApi(Resource):
    def __init__(self):
        self.message_model = Messages()

    def get(self, you_id):
        result = self.message_model.get_last_message(session['id'],
                                                     you_id)
        if result:
            result['message_date'] = str(result['message_date'])
            return {'new_messages': result}, 200
        else:
            return {}, 204


class MessageApi(Resource):
    def __init__(self):
        self.message_model = Messages()

    def get(self, you_id):
        result = self.message_model.check_new_messages(session['id'],
                                                       you_id, checker=True)
        if result:
            for r in result:
                r['message_date'] = str(r['message_date'])
            return {'new_messages': result}, 200
        else:
            return {}, 204

    def post(self, you_id):
        result = self.message_model.add_new_message(session['id'], you_id,
                                                    request.form['message'])
        if result:
            return {'id': session['id'], 'message_date': result}, 201
        else:
            return {}, 204


class MessageNonCheckApi(Resource):
    def __init__(self):
        self.message_model = Messages()

    def get(self, you_id):
        result = self.message_model.check_new_messages(session['id'],
                                                       you_id, checker=False)
        if result:
            for r in result:
                r['message_date'] = str(r['message_date'])
            return {'new_messages': result}, 200
        else:
            return {}, 204
