from flask_restful import Resource, reqparse
from flask import session, make_response
import app.model.user_auth as model
import mysql.connector.errors as dberr


class UserLogin(Resource):
    def __init__(self):
        self.model = model.UserAuth()
        self.parser = reqparse.RequestParser()

    def get(self):
        if 'login' in session:
            return {'login': 1}
        else:
            return {'login': 0}

    def post(self):
        self.parser.add_argument('username')
        self.parser.add_argument('password')
        try:
            argv = self.parser.parse_args()
            if 'username' in argv and 'password' in argv:
                session['login'] = 1
                return self.model.login(argv['username'], argv['password'])
            else:
                return {'login': -1}
        except dberr.Error as err:
            return {'error': "{}".format(err)}

    def delete(self):
        if 'login' in session:
            print(session)
            res = make_response('remove session')
            res.set_cookie('session', '0', max_age=0)
            print(session)
            return {'login': 0}
        else:
            return {'login': -1}


