from flask import Flask
from app.model.model import Model
from mysql.connector.errors import Error as DbError
from operator import itemgetter
import ast


class UserData(Model):
    def __init__(self):
        super(UserData, self).__init__()
        self.cursor = self.matchadb.cursor(dictionary=True)

    def get_users(self, uids, sort_age='False', sort_rating='True'):
        users = list()
        for uid in uids:
            aaa = self.get_data(uid)
            users.append(aaa)
        sort_age = ast.literal_eval(sort_age)
        sort_rating = ast.literal_eval(sort_rating)
        users = sorted(users, key=itemgetter('rating'), reverse=sort_rating)
        users = sorted(users, key=itemgetter('age'), reverse=sort_age)
        return users

    def get_data(self, uid):
        user_data = dict()
        user_data.update(self._get_names(uid))
        user_data.update(self._get_options(uid))
        user_data.update(self._get_biography(uid))
        user_data.update(self._get_geo(uid))
        user_data.update(self._get_rating(uid))
        user_data['tags'] = self._get_tags(uid)
        user_data['photos'] = self._get_photos(uid)
        user_data['id'] = uid
        return user_data

    def _get_names(self, uid):
        self.cursor.execute("SELECT first_name, last_name FROM names WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == -1:
            raise DbError('User not found')
        return data

    def _get_options(self, uid):
        self.cursor.execute(
            "SELECT gender, sex_pref, TIMESTAMPDIFF(year, age, NOW()) as age FROM options WHERE "
            "uid = %s",
            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == -1:
            raise DbError('User not found')
        return data

    def _get_biography(self, uid):
        self.cursor.execute("SELECT biography FROM biographies WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == -1:
            raise DbError('User not found')
        return data

    def _get_geo(self, uid):
        self.cursor.execute("SELECT city, region, country FROM geo WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == -1:
            raise DbError('User not found')
        return data

    def _get_rating(self, uid):
        data = dict()
        self.cursor.execute("SELECT full_profile FROM confirmed WHERE uid = %s",
                            (uid,))
        if self.cursor.fetchone()['full_profile'] == 0:
            return 0
        self.cursor.execute("SELECT COUNT(uid) as count FROM photo_compare "
                            "WHERE uid = %s",(uid,))
        data['photos'] = (self.cursor.fetchone()['count'])

        self.cursor.execute("SELECT COUNT(whomid) as count FROM likes WHERE "
                            "whomid = %s", (uid,))
        data['likes'] = self.cursor.fetchone()['count']

        self.cursor.execute("SELECT COUNT(whomid) as count FROM guests WHERE "
                            "whomid = %s", (uid,))
        data['guests'] = self.cursor.fetchone()['count']
        rating = data['photos'] * 10 + data['likes'] * 12 + data['guests'] * 7
        return {'rating': rating}

    def _get_tags(self, uid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT tag FROM tags WHERE "
                       "uid = %s",
                       (uid,))
        raw_data = cursor.fetchall()
        if cursor.rowcount == -1:
            return 'None'
        data = list()
        for d in raw_data:
            data.append(d[0])
        return data

    def _get_photos(self, uid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT phid FROM photo_compare WHERE "
                       "uid = %s",
                       (uid,))
        raw_data = cursor.fetchall()
        if cursor.rowcount == -1:
            return []
        data = list()
        for d in raw_data:
            data.append(d[0])
        return data
