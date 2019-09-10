from flask import Flask
from flask_mail import Message, Mail
from app.lazy import lazy_async


class MailAgent:
    def __init__(self, app: Flask):
        self.mail = Mail(app)
        self.app = app

    @lazy_async
    def _async_mail(self, msg: Message):
        with self.app.app_context():
            self.mail.send(msg)

    def send_mail(self, msg: Message):
        self._async_mail(msg)
