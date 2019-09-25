import os

from PIL import Image
from app.model.model import Model
import imghdr


class ImageExchange(Model):
    def __init__(self):
        super(ImageExchange, self).__init__()
        self.allow_extension = ['gif', 'jpg', 'jpeg', 'png']

    def upload_img(self, filename, uid):
        self._check_number(uid)
        cursor = self.matchadb.cursor()
        if imghdr.what(filename) not in self.allow_extension:
            raise TypeError('Incorrect type of file')
        self._thumbnail(filename)
        cursor.execute('INSERT INTO photo_data (id, photo) VALUES (NULL, %s)',
                       (self._read_img(filename),))
        phid = cursor.lastrowid
        cursor.execute('INSERT INTO photo_compare (uid, phid) VALUES (%s, %s)',
                       (uid, phid))
        if self._photo_number(uid) > 0:
            self._change_status(uid, 1)
        self._delete_image(filename)

    def download_img(self, phid):
        c = self.matchadb.cursor(dictionary=True)
        c.execute("SELECT photo FROM photo_data WHERE id = %s", (phid,))
        img = c.fetchone()
        return img['photo']

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

    def _thumbnail(self, filename: str):
        im: Image = Image.open(filename)
        im = im.resize((640, 480))
        im.save(filename)

    def _photo_number(self, uid) -> int:
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(phid) as count FROM photo_compare WHERE "
                       "uid = %s",
                       (uid,))
        result = cursor.fetchone()
        return result['count']

    def _change_status(self, uid, status):
        cursor = self.matchadb.cursor()
        cursor.execute("UPDATE confirmed SET photo_is_available = %s WHERE uid "
                       "= %s", (status, uid))

    def _delete_image(self, filename):
        if os.path.exists(filename):
            os.remove(filename)
        else:
            raise FileNotFoundError('Some internal bullshit')

    def delete_image(self, uid, phid):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("DELETE FROM photo_data WHERE id = %s", (phid,))
        cursor.execute("DELETE FROM photo_compare WHERE phid = %s", (phid,))
        cursor.execute("SELECT COUNT(uid) as count FROM photo_compare WHERE "
                       "uid = %s", (uid,))
        result = cursor.fetchone()
        if result['count'] == 0:
            self.change_status(photo=0)
