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

    def mail_confirm(self, seed):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute(
            "SELECT uid FROM changes WHERE seed = %s and reason = 100",
            (seed,))
        user = cursor.fetchone()
        if cursor.rowcount <= 0 :
            raise NameError("Seed not found")
        cursor.execute("UPDATE confirmed SET confirm_email = TRUE WHERE uid = "
                       "%s", (user['uid'],))
        cursor.execute("DELETE FROM changes WHERE uid = %s", (user['uid'],))

