import app.model.model as model
import hashlib


class UserAuth(model.Model):
    def login(self, username, password):
        cursor = self.matchadb.cursor(dictionary=True)
        query = (
            username,
            hashlib.sha3_512(password.encode('utf-8')).hexdigest()
        )
        cursor.execute("SELECT id FROM users WHERE username = %s and password = %s", query)
        cursor.fetchone()
        if cursor.rowcount > 0:
            return {'login': 1}
        else:
            return {'login': 0}
