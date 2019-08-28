from flask import Flask

from app.model.model import Model
import imghdr


class ImageExchange(Model):
    def __init__(self, app: Flask):
        super(ImageExchange, self).__init__(app)
        self.allow_extension = ['gif', 'jpg', 'jpeg', 'png']

    def upload_img(self, filename, uid):
        self._check_number(uid)
        cursor = self.matchadb.cursor()
        if imghdr.what(filename) not in self.allow_extension:
            raise TypeError('Incorrect type of file')
        cursor.execute('INSERT INTO photo_data (id, photo) VALUES (NULL, %s)',
                       (self._read_img(filename),))
        phid = cursor.lastrowid
        cursor.execute('INSERT INTO photo_compare (uid, phid) VALUES (%s, %s)',
                       (uid, phid))

    def _check_number(self, uid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT COUNT(uid) FROM photo_compare WHERE uid = %s",
                       (uid,))
        num = cursor.fetchone()
        if num[0] >= 5:
            raise ValueError('Too many photo')

    def _read_img(self, filename):
        with open(filename, 'rb') as file:
            binary_data = file.read()
        return binary_data
