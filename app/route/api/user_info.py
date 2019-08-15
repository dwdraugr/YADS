from flask_restful import Resource
import app.model.api.api_user_data as api
import mysql.connector.errors as dberr


class UidGet(Resource):
    def __init__(self):
        self.model = api.ApiGetModel()

    def get(self, uid, data_type=None):
        try:
            if data_type is None:
                return {'biba', 'sasiba'}
            elif data_type == 'age':
                return self.model.get_user_age(uid)
            elif data_type == 'gender':
                return self.model.get_user_gender(uid)
            elif data_type == 'sex_pref':
                return self.model.get_user_sex_pref(uid)
            elif data_type == 'biography':
                return self.model.get_user_biography(uid)
            elif data_type == 'tags':
                return self.model.get_user_tags(uid)
            elif data_type == 'photos':
                return self.model.get_user_photos(uid)
            elif data_type == 'rating':
                return self.model.get_user_rating(uid)
            elif data_type == 'geo':
                return self.model.get_user_geo(uid)
            elif data_type == 'online':
                return self.model.get_user_online(uid)
            elif data_type == 'name':
                return self.model.get_user_first_last_names(uid)
        except NameError as err:
            return {'error': "{}".format(err)}, 404
        except dberr.Error as err:
            return {'error': "{}".format(err)}, 500
