from app.model.model import Model


class CompareUsers(Model):
    def get_compare_users(self, uid):
        cursor = self.matchadb.cursor()
        cursor.execute('SELECT whomid FROM likes WHERE whoid = %s', (uid,))
        whomids = [item[0] for item in cursor.fetchall()]
        if len(whomids) == 0:
            raise ValueError('Likes not found')
        result = list()
        for whomid in whomids:
            cursor.execute('SELECT whomid FROM likes WHERE whoid = %s AND '
                           'whomid = %s', (uid, whomid))
            r = cursor.fetchone()
            if cursor.rowcount > 0:
                result.append(r[0])
        return result
