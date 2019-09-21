from app.model.model import Model
from flask_mail import Message
from flask import request, render_template, Flask
import hashlib, re, random, string

from app.model.mail_agent import MailAgent


class SignUp(Model):
    def __init__(self, app: Flask):
        super(SignUp, self).__init__()
        self.mail = MailAgent(app)

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
        self.mail.send_mail(msg)

    def _check_email(self, email):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT id from users WHERE email = %s", (email,))
        if cursor.fetchone() is not None:
            raise NameError('User with this email exist')

    def _check_username(self, username):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone() is not None:
            raise NameError('User with this username exist')

