import app.model.model as model
import hashlib


class UserSignup(model.Model):
    def __init__(self):
        super(UserSignup, self).__init__()

    def signup(self, username, password, email):
        cursor = self.matchadb.cursor(dictionary=True)
        query = [
            username,
            email,
        ]
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", tuple(query))
        data = cursor.fetchall()
        if cursor.rowcount == 0:
            query.append(hashlib.sha3_512(password.encode('utf-8')).hexdigest())
            cursor.execute("INSERT INTO users (id, username, password, email) VALUES "
                           "(NULL, %s, %s, %s)", tuple(query))
            cursor.execute()