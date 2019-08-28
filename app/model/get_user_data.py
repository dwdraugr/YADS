from flask import Flask
from app.model.model import Model
from mysql.connector.errors import Error as DbError


class UserData(Model):
    def __init__(self, app: Flask):
        super(UserData, self).__init__(app)
        self.cursor = self.matchadb.cursor(dictionary=True)

    def get_data(self, uid):
        user_data = {
            **self._get_names(uid),
            **self._get_options(uid),
            **self._get_biography(uid),
            **self._get_geo(uid),
            **self._get_rating(uid),
            'tags': self._get_tags(uid)
        }
        return user_data

    def _get_names(self, uid):
        self.cursor.execute("SELECT first_name, last_name FROM names WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == 0:
            raise DbError('User not found')
        return data

    def _get_options(self, uid):
        self.cursor.execute("SELECT gender, sex_pref, age FROM options WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == 0:
            raise DbError('User not found')
        return data

    def _get_biography(self, uid):
        self.cursor.execute("SELECT biography FROM biographies WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == 0:
            raise DbError('User not found')
        return data

    def _get_geo(self, uid):
        self.cursor.execute("SELECT city, region, country FROM geo WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == 0:
            raise DbError('User not found')
        return data

    def _get_rating(self, uid):
        self.cursor.execute("SELECT rating FROM ratings WHERE "
                            "uid = %s",
                            (uid,))
        data = self.cursor.fetchone()
        if self.cursor.rowcount == 0:
            raise DbError('User not found')
        return data

    def _get_tags(self, uid):
        self.cursor = self.matchadb.cursor()
        self.cursor.execute("SELECT tag FROM tags WHERE "
                            "uid = %s",
                            (uid,))
        raw_data = self.cursor.fetchall()
        if self.cursor.rowcount == 0:
            raise DbError('User not found')
        data = list()
        for d in raw_data:
            data.append(d[0])
        return data
