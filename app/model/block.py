from app.model.model import Model


class Block(Model):
    def __init__(self):
        super(Block, self).__init__()
        self.cursor = self.matchadb.cursor()

    def get_block(self, whoid, whomid):
        self.cursor.execute("SELECT whomid FROM block WHERE whoid = %s AND "
                            "whomid = %s", (whoid, whomid))
        self.cursor.fetchone()
        if self.cursor.rowcount <= 0:
            return False
        else:
            return True

    def block_user(self, whoid, whomid):
        self.cursor.execute("SELECT whomid FROM block WHERE whoid = %s AND "
                            "whomid = %s", (whoid, whomid))
        self.cursor.fetchone()
        if self.cursor.rowcount != 1:
            self.cursor.execute("INSERT INTO block (whoid, whomid) VALUES "
                                "(%s, %s)", (whoid, whomid))
            return True
        else:
            return False

    def unblock_user(self, whoid, whomid):
        self.cursor.execute("SELECT whomid FROM block WHERE whoid = %s AND "
                            "whomid = %s", (whoid, whomid))
        self.cursor.fetchone()
        if self.cursor.rowcount == 1:
            self.cursor.execute("DELETE FROM block WHERE whoid = %s and "
                                "whomid = %s", (whoid, whomid))
            return True
        else:
            return False
