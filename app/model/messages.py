from flask import session
from app.model.model import Model
from mysql.connector import Error as DbError


class Messages(Model):
    def get_messages(self, interlocutor_id):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT id, text, sender, receiver, message_date "
                       "FROM messages WHERE (sender = %s AND receiver = %s) "
                       "OR (sender = %s AND receiver = %s) "
                       "ORDER BY message_date ASC",
                       (session['id'], interlocutor_id, interlocutor_id,
                        session['id']))
        messages = cursor.fetchall()
        cursor.execute("UPDATE messages SET message_read = TRUE WHERE "
                       "sender = %s AND receiver = %s and message_read = "
                       "FALSE", (interlocutor_id, session['id']))
        return messages

    def get_data(self, interlocutor_id):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT uid, first_name, last_name FROM names WHERE "
                       "uid = %s",
                       (session['id'],))
        my_data = cursor.fetchone()
        cursor.execute("SELECT uid, first_name, last_name FROM names WHERE "
                       "uid = %s",
                       (interlocutor_id,))
        interlocutor_data = cursor.fetchone()

        cursor = self.matchadb.cursor(buffered=True)
        cursor.execute("SELECT phid FROM photo_compare WHERE uid = %s",
                       (session['id'],))
        phid = cursor.fetchone()
        my_data['phid'] = phid[0] if phid is not None else None

        cursor.execute("SELECT phid FROM photo_compare WHERE uid = %s",
                       (interlocutor_id,))
        phid = cursor.fetchone()
        interlocutor_data['phid'] = phid[0] if phid is not None else None

        return my_data, interlocutor_data

    def check_new_messages(self, my_id, you_id, checker=False):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT text, sender, receiver, message_date "
                       "FROM messages WHERE sender = %s AND receiver = %s AND "
                       "message_read = FALSE ORDER BY message_date ASC",
                       (you_id, my_id))
        data = cursor.fetchall()
        if cursor.rowcount > 0 is None:
            return False
        elif checker:
            cursor.execute("UPDATE messages SET message_read = TRUE WHERE "
                           "sender = %s AND receiver = %s and message_read = "
                           "FALSE", (you_id, my_id))
            return data
        else:
            return data

    def check_all_new_message(self, my_id):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(sender) as count "
                       "FROM messages WHERE receiver = %s AND "
                       "message_read = FALSE ORDER BY message_date ASC",
                       (my_id,))
        data = cursor.fetchall()
        if cursor.rowcount > 0 is None:
            return False
        else:
            return data

    def get_last_message(self, my_id, you_id):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("SELECT text, sender, receiver, message_date "
                       "FROM messages WHERE (sender = %s AND receiver = %s) "
                                        "OR (sender = %s AND receiver = %s) "
                       "ORDER BY message_date DESC",
                       (you_id, my_id, my_id, you_id))
        data = cursor.fetchone()
        if data is None:
            return False
        else:
            return data

    def add_new_message(self, my_id, you_id, message):
        try:
            cursor = self.matchadb.cursor()
            cursor.execute("INSERT INTO messages (id, text, sender, receiver, "
                           "message_read, message_date) VALUES (NULL, %s, %s, "
                           "%s, "
                           "0, NOW())", (message, my_id, you_id))
            cursor.execute("SELECT NOW() as time")
            result = cursor.fetchone()
            return str(result[0])
        except DbError:
            return False
