import mysql.connector


class Model:
    def __init__(self):
        self.matchadb = mysql.connector.connect(
            host="192.168.99.100",
            user="root",
            passwd="qwerty",
            database='matcha',
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            autocommit=True
        )

    def _get_geo_address(self, ip):
        return "http://api.ipstack.com/" + ip + "?access_key" \
                                                "=ded7e893c0fd5a1f641aef3" \
                                                "a3f2287d7"
