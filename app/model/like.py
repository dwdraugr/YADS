from app.model.model import Model


class Like(Model):
    def add_like(self, whoid, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (whomid,))
        cursor.fetchone()
        if cursor.rowcount < 1:
            return False
        cursor.execute("SELECT * FROM likes WHERE whoid = %s AND whomid = %s",
                       (whoid, whomid))
        cursor.fetchall()
        if cursor.rowcount <= 0:
            cursor.execute("INSERT INTO likes (whoid, whomid) VALUES (%s, %s)",
                           (whoid, whomid))
            return True
        else:
            return False

    def find_like(self, whoid, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT * FROM likes WHERE whoid = %s AND whomid = %s",
                       (whoid, whomid))
        cursor.fetchone()
        if cursor.rowcount < 1:
            return False
        else:
            return True

    def delete_like(self, whoid, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("DELETE FROM likes WHERE whoid = %s and whomid = %s",
                       (whoid, whomid))
        if cursor.rowcount > 0:
            return True
        else:
            return False
