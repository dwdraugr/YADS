from flask import Flask

from model import Model
from flask_mail import Mail
import hashlib, re, os


class SignUp(Model):
    def __init__(self, app):
        super(SignUp, self).__init__()
        app.config.update(
            MAIL_SERVER='smtp.gmail.com',
            MAIL_PORT=587,
            MAIL_USE_TLS=True,
            MAIL_USERAME=os.environ.get('GMAIL_ADDR'),
            MAIL_PASSWORD=os.environ.get('GMAIL_PASS')
        )
        self.mail = Mail(app)

    def sign_up(self, username, email, password):
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
        self._send_mail(email)

    def _send_mail(self, email):
        msg = self.mail.send_message(
            'Tutor mail',
            sender='kostya.marinenkov@gmail.com',
            recipients=[email],
            body='EEEE BOUUUU'
        )


