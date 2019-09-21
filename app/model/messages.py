from flask import session
from app.model.model import Model


class Messages(Model):
    def get_messages(self, interlocutor_id):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT text, sender, receiver, message_date "
                       "FROM messages WHERE (sender = %s AND receiver = %s) "
                                        "OR (sender = %s AND receiver = %s)",
                       (session['id'], interlocutor_id, interlocutor_id, session['id']))
        messages = cursor.fetchall()
        return messages

    def get_data(self, interlocutor_id):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT first_name, last_name FROM names WHERE uid = %s", (session['id'],))
        my_data = cursor.fetchone()
        cursor.execute("SELECT first_name, last_name FROM names WHERE uid = %s", (interlocutor_id,))
        interlocutor_data = cursor.fetchone()

        cursor = self.matchadb.cursor(buffered=True)
        cursor.execute("SELECT phid FROM photo_compare WHERE uid = %s", (session['id'],))
        phid = cursor.fetchone()
        my_data['phid'] = phid[0] if phid is not None else None

        cursor.execute("SELECT phid FROM photo_compare WHERE uid = %s", (interlocutor_id,))
        phid = cursor.fetchone()
        interlocutor_data['phid'] = phid[0] if phid is not None else None

        return my_data, interlocutor_data

    def add_message(self, message_id, text, sender, receiver):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s OR id = %s", (sender, receiver))
        cursor.fetchone()
        if cursor.rowcount < 2:
            return False
        cursor.execute("SELECT id FROM messages WHERE id = %s", (message_id,))
        cursor.fetchall()
        if cursor.rowcount <= 0:
            cursor.execute("INSERT INTO messages (text, sender, receiver, message_read, message_date)"
                           "VALUES (%s, %s, %s, False, NOW())", (text, sender, receiver))
            return True
        else:
            return False

    def find_message(self, message_id):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT text, receiver, message_date FROM messages WHERE id = %s", (message_id,))
        cursor.fetchone()
        if cursor.rowcount < 1:
            return False
        else:
            return
