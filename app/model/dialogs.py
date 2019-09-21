from flask import session
from app.model.model import Model


class Dialogs(Model):
    def get_contacts(self):
        cursor = self.matchadb.cursor()
        cursor.execute('SELECT whomid FROM likes WHERE whoid = %s', (session['id'],))
        contacts = [item[0] for item in cursor.fetchall()]

        cursor = self.matchadb.cursor(buffered=True, dictionary=True)
        result = list()
        for contact in contacts:
            cursor.execute('SELECT likes.whoid, names.first_name, names.last_name, photo_compare.phid '
                           'FROM likes '
                           'JOIN names ON names.uid = %s '
                           'LEFT JOIN photo_compare ON photo_compare.uid = %s '
                           'WHERE likes.whoid = %s AND likes.whomid = %s', (contact, contact, contact, session['id']))
            r = cursor.fetchone()
            if cursor.rowcount > 0:
                result.append(r)

        contacts = result
        return contacts
