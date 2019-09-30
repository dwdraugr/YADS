from flask import session
from app.model.model import Model
import mysql.connector as sql
import hashlib


class GeneralSettings(Model):
    def update_settings(self, data: dict):
        message = ''
        name_mess = self._update_names(data['first'], data['last'])
        opt_mess = self._update_options(data['gender'], data['sex_pref'], data['age'])
        bio_mess = self._update_biography(data['biography'])
        tags_mess = self._update_tags(data['tags'])
        if name_mess is not None:
            message += name_mess
        for o in opt_mess:
            if message != '':
                message += ', ' + o
            else:
                message += o
        if bio_mess is not None:
            if message != '':
                message += ', ' + bio_mess
            else:
                message += bio_mess
        if tags_mess is not None :
            if message != '':
                message += ', ' + tags_mess
            else:
                message += tags_mess
        return message + ' change success!'

    def _update_names(self, first='', last=''):
        cursor = self.matchadb.cursor(dictionary=True)
        if first and last != '':
            cursor.execute(
                "UPDATE names SET first_name = %s, last_name = %s WHERE uid = "
                "%s",
                (first, last, session['id']))
            return 'First and Last names'
        elif first is not None and first != '':
            cursor.execute(
                "UPDATE names SET first_name = %s WHERE uid = %s",
                (first, session['id']))
            return 'First name'
        elif last is not None and last != '':
            cursor.execute(
                "UPDATE names SET last_name = %s WHERE uid = %s",
                (last, session['id']))
            return 'Last name'
        else:
            return None
        # if cursor.rowcount == 0:
        #     raise sql.errors.Error('Unable to write in database')

    def _update_options(self, gender, sex_pref, age):
        cursor = self.matchadb.cursor(dictionary=True)
        message = list()
        if gender is not None and gender != '':
            cursor.execute(
                "UPDATE options SET gender = %s WHERE uid = %s",
                (gender, session['id']))
            message.append('Gender')
        if sex_pref is not None and sex_pref != '':
            cursor.execute(
                "UPDATE options SET sex_pref = %s WHERE uid = %s",
                (sex_pref, session['id']))
            message.append('Sex preference')
        if age is not None and age != '':
            cursor.execute(
                "UPDATE options SET age = %s WHERE uid = %s",
                (age, session['id']))
            message.append('Age')
        return message
        # if cursor.rowcount == 0:
        #     raise sql.errors.Error('Unable to write in database')

    def _update_biography(self, biography):
        cursor = self.matchadb.cursor(dictionary=True)
        if biography is not None and biography != '':
            cursor.execute(
                "UPDATE biographies SET biography = %s WHERE uid = %s",
                (biography, session['id']))
            return 'Biography'
        return None
        # if cursor.rowcount == 0:
        #     raise sql.errors.Error('Unable to write in database')

    def _update_tags(self, tags: list):
        cursor = self.matchadb.cursor(dictionary=True)
        if len(tags) != 0:
            cursor.execute("DELETE FROM tags WHERE uid = %s", (session['id'],))
            for tag in tags:
                cursor.execute("INSERT INTO tags (uid, tag) VALUES (%s, %s)",
                               (session['id'], tag))
            return 'Tags'
        return None
            # if cursor.rowcount == 0:
            #     raise sql.errors.Error('Unable to write in database')


class EmailSettings(Model):
    def update_settings(self, new_email):
        self._check_emails_match(new_email)
        cursor = self.matchadb.cursor()
        cursor.execute("UPDATE users SET email = %s WHERE id = %s",
                       (new_email, session['id']))
        return 'Email change successfully'

    def _check_emails_match(self, new_email):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT email FROM users WHERE email = %s", (new_email,))
        cursor.fetchone()
        if cursor.rowcount > 0:
            raise NameError("Email already exists")


class PasswordSettings(Model):
    def update_settings(self, old_password, new_password):
        old_password = hashlib.sha3_512(
            old_password.encode('utf-8')).hexdigest()
        new_password = hashlib.sha3_512(
            new_password.encode('utf-8')).hexdigest()

        self._check_old_password(old_password)

        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute(
            "UPDATE users SET password = %s WHERE password = %s AND id = %s",
            (new_password, old_password, session['id']))
        return 'Password change successfully'

    def _check_old_password(self, old_password):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute(
            "SELECT password FROM users WHERE password = %s and id = %s",
            (old_password, session['id']))
        cursor.fetchone()
        if cursor.rowcount < 1:
            raise NameError("Wrong old password")