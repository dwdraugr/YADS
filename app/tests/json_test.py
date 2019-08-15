import mysql.connector

mydb = mysql.connector.connect(
    host="192.168.99.100",
    user="root",
    passwd="qwerty",
    database="matcha"
)
cur = mydb.cursor(dictionary=True)
cur.execute("SELECT * FROM users WHERE id = 1")
user = cur.fetchone()
cur = mydb.cursor()
cur.execute("SELECT * FROM tags WHERE uid = 1;")
data = cur.fetchall()
jsons = list()
for id, tag in data:
    jsons.append(tag)
print(jsons)
user['tags'] = jsons
print(user)
