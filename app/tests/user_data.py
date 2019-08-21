import app.core.model as model
from datetime import datetime


class ApiGetModel(model.Model):
    def __init__(self):
        super().__init__()

    def get_user_first_last_names(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT first_name, last_name FROM names WHERE uid = %s;", (uid,))
        data = cursor.fetchone()
        if data is not None and len(data) > 0:
            return data
        else:
            raise NameError('id not found')

    def get_user_age(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT age FROM options WHERE uid = %s;", (uid,))
        data = cursor.fetchone()
        if data is not None and len(data) > 0:
            return data
        else:
            raise NameError('id not found')

    def get_user_gender(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT gender FROM options WHERE uid = %s;", (uid,))
        data = cursor.fetchone()
        if data is not None and len(data) > 0:
            return data
        else:
            raise NameError('id not found')

    def get_user_sex_pref(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT sex_pref FROM options WHERE uid = %s;", (uid,))
        data = cursor.fetchone()
        if data is not None and len(data) > 0:
            return data
        else:
            raise NameError('id not found')

    def get_user_biography(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT biography FROM biographies WHERE uid = %s;", (uid,))
        data = cursor.fetchone()
        if data is not None and len(data) > 0:
            return data
        else:
            raise NameError('id not found')

    def get_user_tags(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT tag FROM tags WHERE uid = %s;", (uid,))
        data = cursor.fetchall()
        result = list()
        if data is not None and len(data):
            for tag in data:
                result.append(tag)
            return {'tags': data}
        else:
            raise NameError('id not found')

    def get_user_geo(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT country, region, city, gps_geo FROM geo WHERE uid = %s;", (uid,))
        data = cursor.fetchone()
        if data is not None and len(data) > 0:
            return data
        else:
            raise NameError('id not found')

    def get_user_photos(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM photo_compare WHERE uid = %s;", (uid,))
        data = list()
        if cursor.rowcount > 0:
            for iid, tag in cursor.fetchall():
                data.append(tag)
            return {'photos': data}
        else:
            return {'error': 'photo not found'}

    def get_user_rating(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT rating FROM ratings WHERE uid = %s;", (uid,))
        data = cursor.fetchone()
        if data is not None and len(data) > 0:
            return data
        else:
            raise NameError('id not found')

    def get_user_online(self, uid):
        cursor = self.matchadb.cursor(dictionary=True)
        now = datetime.now()
        format_date = now.strftime('%Y-%m-%d %H:%M:%s')
        cursor.execute("SELECT * FROM online WHERE uid = %s AND time_until > %s;", (uid, format_date))
        cursor.fetchall()
        if cursor.rowcount > 0:
            return {'status': 'online'}
        else:
            return {'status': 'offline'}
