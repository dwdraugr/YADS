import mysql.connector
from flask import Flask, session
from flask_mail import Mail, Message

from app.lazy import lazy_async

all_tags = (
    'Hunting',
    'Fishing',
    'Signing',
    'Fuck porcupine',
    'Watching "Разведопрос"'
)


class Model:
    def __init__(self):
        self.matchadb = mysql.connector.connect(
            host="192.168.99.102",
            user="root",
            passwd="qwerty",
            database='matcha',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            autocommit=True
        )

    def _get_geo_address(self, ip):
        return "http://api.ipstack.com/" + ip + "?access_key" \
                                                "=ded7e893c0fd5a1f641aef3" \
                                                "a3f2287d7"

    def change_status(self, uid: int = -1,
                      email: int = -1, profile: int = -1, photo: int = -1):
        cursor = self.matchadb.cursor()
        if 'id' in session:
            if email == -1:
                email = session['confirm_email']
            if profile == -1:
                profile = session['full_profile']
            if photo == -1:
                photo = session['photo_is_available']
            cursor.execute("UPDATE confirmed SET"
                           "confirm_email = %s, full_profile = %s,"
                           "photo_is_available = %s WHERE uid = %s",
                           (email, profile, photo, session['id']))
            if cursor.rowcount == 0:
                raise NameError('Incorrect request: uid is unavailable')
        elif email != -1 and uid != -1:
            cursor.execute("UPDATE confirmed SET confirm_email = %s WHERE "
                           "uid = %s", (1, uid))
            if cursor.rowcount == 0:
                raise NameError('Incorrect request: uid is unavailable')
        else:
            raise RuntimeError("!Warning! This method not work in request "
                               "context")
