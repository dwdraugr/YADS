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
        cursor.execute("SELECT confirm_email, full_profile, "
                       "photo_is_available FROM confirmed WHERE uid = %s",
                       (session['id'],))
        result = cursor.fetchone()
        session['confirm_email'] = result['confirm_email']
        session['full_profile'] = result['full_profile']
        session['photo_is_available'] = result['photo_is_available']
        if session['confirm_email'] == 0:
            session.clear()
            raise NameError('User is not confirmed')

    def sign_out(self):
        session.clear()

    def mail_confirm(self, seed):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute(
            "SELECT uid FROM changes WHERE seed = %s and reason = 100",
            (seed,))
        user = cursor.fetchone()
        if cursor.rowcount <= 0:
            raise NameError("Seed not found")
        self.change_status(uid=user['uid'], email=1)
        cursor.execute("DELETE FROM changes WHERE uid = %s", (user['uid'],))
