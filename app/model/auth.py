from app.model.model import Model
from flask import session
import hashlib


class Auth(Model):
    def sign_in(self, username, password):
        cursor = self.matchadb.cursor(dictionary=True)
        query = (
            username,
            hashlib.sha3_512(password.encode('utf-8')).hexdigest()
        )
        cursor.execute("SELECT id, username FROM users WHERE username = %s "
                       "and password = %s", query)
        result = cursor.fetchone()
        if cursor.rowcount > 0:
            session['id'] = result['id']
            session['username'] = result['username']
        else:
            raise NameError('User Not Found')

    def sign_out(self):
        session.clear()
