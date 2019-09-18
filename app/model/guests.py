from app.model.model import Model


class GuestsCheck(Model):
    def get_guests(self, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT whoid FROM guests WHERE whomid = %s AND check_g = 0 ORDER BY \
                        guest_date DESC",
                       (whomid,))
        guests = [item[0] for item in cursor.fetchall()]
        if len(guests) == 0:
            return False
        else:
            return guests

    def add_guest(self, whoid, whomid):
        if whomid == whoid:
            return False
        cursor = self.matchadb.cursor()
        cursor.execute(
            "SELECT whoid FROM guests WHERE DAY(guest_date) = DAY(NOW()) AND "
            "whoid = %s AND whomid = %s", (whoid, whomid))
        cursor.fetchone()
        if cursor.rowcount == 1:
            return False
        cursor.execute("INSERT INTO guests (id, whoid, whomid, guest_date, check_g)"
                       "VALUES (NULL, %s, %s, NOW(), FALSE)", (whoid, whomid))
        return True

    def check_guest(self, whomid):
        cursor = self.matchadb.cursor()
        cursor.execute("UPDATE guests SET check_g = 1 WHERE whomid = %s",
                       (whomid,))

