from flask_restful import Resource
from app.model.lazy_model import *


class UidAll(Resource):
    def get(self, uid, data_type=None):
        if data_type is None:
            return get_all()
        elif data_type == 'age':
            return get_age()
        elif data_type == 'gender':
            return get_gender()
        elif data_type == 'sex_pref':
            return get_sex_pref()
        elif data_type == 'biography':
            return get_biography()
        elif data_type == 'tags':
            return get_tags()
        elif data_type == 'photos':
            return get_photos()
