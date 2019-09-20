from app.model.model import Model


class Online(Model):
    def set_online(self, uid):
        cursor = self.matchadb.cursor()
        cursor.execute("REPLACE INTO online (uid, time_until)"
                       "VALUES (%s, NOW() + INTERVAL 30 MINUTE)", (uid,))

    def get_online(self, uid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT time_until FROM online WHERE time_until > NOW()"
                       " and uid = %s", (uid,))
        data = cursor.fetchone()
        if data is not None:
            return 'Online'
        cursor.execute("SELECT time_until FROM online WHERE uid = %s", (uid,))
        data = cursor.fetchone()
        if data is not None:
            return data[0]
        else:
            return False
