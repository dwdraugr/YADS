from app.lazy import lazy_async
from app.model.model import Model
from flask_mail import Mail, Message
from flask import request, render_template
import hashlib, re, random, string


class SignUp(Model):
    def sign_up(self, username, email, password):
        self._check_email(email)
        self._check_username(username)
        cursor = self.matchadb.cursor(dictionary=True)
        result = re.fullmatch("^[a-zA-Z][a-zA-Z0-9_]*$", username)
        if not result:
            raise NameError("Username of new user is invalid")
        query = (
            username,
            hashlib.sha3_512(password.encode('utf-8')).hexdigest(),
            email
        )
        cursor.execute("INSERT INTO users (id, username,"
                       "password, email) VALUE (NULL, %s, %s, %s)", query)
        new_user = cursor.lastrowid
        cursor.execute("INSERT INTO confirmed (uid, confirm_email, "
                       "full_profile, photo_is_available) VALUES (%s, FALSE , "
                       "FALSE , FALSE )",
                       (new_user,))
        query = (
            new_user,
            ''.join(random.choice(string.ascii_letters) for i in range(30))
        )
        cursor.execute("INSERT INTO changes (uid, reason, seed) VALUES (%s, "
                       "100, %s)", query)

        msg = Message('Welcome to the YADS!', [email])
        link = request.url_root + 'confirm/new/' + query[1]
        msg.html = render_template('mail_new_account.html', link=link)
        self._send_mail(msg)

    def _check_email(self, email):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT id from users WHERE email = %s", (email,))
        cursor.fetchone()
        if cursor.rowcount > 0:
            raise NameError('User with this email exist')

    def _check_username(self, username):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        cursor.fetchone()
        if cursor.rowcount > 0:
            raise NameError('User with this username exist')

