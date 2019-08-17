from flask_restful import Resource, reqparse
from flask import session
import app.model.user_auth as model
import mysql.connector.errors as dberr

class UserLogin(Resource):
    def __init__(self):
        self.model = model.UserAuth()
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('username')
        self.parser.add_argument('password')
        self.parser.add_argument('e-mail')
