from app.model.model import Model


class Like(Model):
    def add_like(self, whoid, whomid):
        cursor = self.matchadb.cursor()
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT COUNT(uid) as count FROM photo_compare WHERE "
                       "uid = %s",
                       (whoid,))
        num = cursor.fetchone()
        if num[0] == 0:
            raise ValueError('No photo - no like')
        cursor.execute("SELECT id FROM users WHERE id = %s", (whomid,))
        cursor.fetchone()
        if cursor.rowcount < 1:
            return False
        cursor.execute("SELECT * FROM likes WHERE whoid = %s AND whomid = %s",
                       (whoid, whomid))
        cursor.fetchall()
        if cursor.rowcount <= 0:
            cursor.execute("INSERT INTO likes (whoid, whomid, check_l) VALUES "
                           "(%s, %s, 0)", (whoid, whomid))
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

    def uncheck_like(self, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT whoid FROM likes WHERE check_l = 0 and whomid "
                       "= %s", (whomid,))
        return [item[0] for item in cursor.fetchall()]

    def check_like(self, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("UPDATE likes SET check_l = 1 WHERE whomid = %s",
                       (whomid,))

    def delete_like(self, whoid, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("DELETE FROM likes WHERE whoid = %s and whomid = %s",
                       (whoid, whomid))
        if cursor.rowcount > 0:
            return True
        else:
            return False
