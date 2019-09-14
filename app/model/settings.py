from flask import session
from app.model.model import Model
import mysql.connector as sql
import hashlib


class GeneralSettings(Model):
    def update_settings(self, data: dict):
        self._update_names(data['first'], data['last'])
        self._update_options(data['gender'], data['sex_pref'], data['age'])
        self._update_biography(data['biography'])
        self._update_tags(data['tags'])

    def _update_names(self, first, last):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("UPDATE names SET first_name = %s, last_name = %s WHERE uid = %s",
                       (first, last, session['id']))
        # if cursor.rowcount == 0:
        #     raise sql.errors.Error('Unable to write in database')

    def _update_options(self, gender, sex_pref, age):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("UPDATE options SET gender = %s, sex_pref = %s, age = %s WHERE uid = %s",
                       (gender, sex_pref, age, session['id']))
        # if cursor.rowcount == 0:
        #     raise sql.errors.Error('Unable to write in database')

    def _update_biography(self, biography):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("UPDATE biographies SET biography = %s WHERE uid = %s",
                       (biography, session['id']))
        # if cursor.rowcount == 0:
        #     raise sql.errors.Error('Unable to write in database')

    def _update_tags(self, tags: list):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("DELETE FROM tags WHERE uid = %s", (session['id'],))
        for tag in tags:
            cursor.execute("INSERT INTO tags (uid, tag) VALUES (%s, %s)",
                           (session['id'], tag))
            # if cursor.rowcount == 0:
            #     raise sql.errors.Error('Unable to write in database')

class EmailSettings(Model):
    def update_settings(self, new_email):
        self._check_emails_match(new_email)
        cursor = self.matchadb.cursor()
        cursor.execute("UPDATE users SET email = %s WHERE id = %s", (new_email, session['id']))

    def _check_emails_match(self, new_email):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT email FROM users WHERE email = %s", (new_email,))
        cursor.fetchone()
        if cursor.rowcount > 0:
            raise NameError("Email already exists")

class PasswordSettings(Model):
    def update_settings(self, old_password, new_password):
        old_password = hashlib.sha3_512(old_password.encode('utf-8')).hexdigest()
        new_password = hashlib.sha3_512(new_password.encode('utf-8')).hexdigest()

        self._check_old_password(old_password)

        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("UPDATE users SET password = %s WHERE password = %s AND id = %s",
                       (new_password, old_password, session['id']))

    def _check_old_password(self, old_password):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT password FROM users WHERE password = %s and id = %s",
                       (old_password, session['id']))
        cursor.fetchone()
        if cursor.rowcount < 1:
            raise NameError("Wrong old password")