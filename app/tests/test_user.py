import mysql.connector

sql_creates = {}

sql_creates['db'] = "CREATE DATABASE IF NOT EXISTS matcha CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sql_creates['usedb'] = 'use matcha;'
sql_creates['users'] = 'CREATE TABLE IF NOT EXISTS users( ' \
                       'id INT AUTO_INCREMENT PRIMARY KEY, ' \
                       'username VARCHAR(30) NOT NULL, ' \
                       'password VARCHAR(1024) NOT NULL, ' \
                       'email VARCHAR(40) NOT NULL);'
sql_creates['names'] = 'CREATE TABLE IF NOT EXISTS names( ' \
                       'uid INT UNIQUE NOT NULL, ' \
                       'first_name VARCHAR(40) NOT NULL, ' \
                       'last_name VARCHAR(45) NOT NULL);'
sql_creates['options'] = 'CREATE TABLE IF NOT EXISTS options(' \
                         'uid INT UNIQUE NOT NULL, ' \
                         'gender VARCHAR(30) NOT NULL, ' \
                         'sex_pref VARCHAR(30) NOT NULL, ' \
                         'age DATE NOT NULL);'
sql_creates['biographies'] = 'CREATE TABLE IF NOT EXISTS biographies( ' \
                             'uid INT UNIQUE NOT NULL, ' \
                             'biography VARCHAR(1000) NOT NULL);'
sql_creates['ratings'] = 'CREATE TABLE IF NOT EXISTS ratings( ' \
                         'uid INT UNIQUE NOT NULL, ' \
                         'rating INT NOT NULL);'
sql_creates['geo'] = 'CREATE TABLE IF NOT EXISTS geo(' \
                     'uid INT UNIQUE NOT NULL, ' \
                     'country VARCHAR(40), ' \
                     'region VARCHAR(40), ' \
                     'city VARCHAR(40), ' \
                     'gps_geo varchar(100));'
sql_creates['photos_data'] = 'CREATE TABLE IF NOT EXISTS photo_data(' \
                        'id INT AUTO_INCREMENT PRIMARY KEY,' \
                        'photo MEDIUMBLOB NOT NULL);'
sql_creates['photos_compare'] = 'CREATE TABLE IF NOT EXISTS photo_compare(' \
                                'uid INT NOT NULL,' \
                                'phid INT NOT NULL);'
sql_creates['tags'] = 'CREATE TABLE IF NOT EXISTS tags(' \
                      'uid INT NOT NULL,' \
                      'tag VARCHAR(30) NOT NULL);'
sql_creates['messages'] = 'CREATE TABLE IF NOT EXISTS messages(' \
                          'id INT AUTO_INCREMENT PRIMARY KEY,' \
                          'text VARCHAR(280) NOT NULL ,' \
                          'sender INT NOT NULL ,' \
                          'receiver INT NOT NULL ,' \
                          'message_read bool DEFAULT FALSE NOT NULL, ' \
                          'message_date DATETIME NOT NULL );'
sql_creates['likes'] = 'CREATE TABLE IF NOT EXISTS likes(' \
                       'whoid INT NOT NULL,' \
                       'whomid INT NOT NULL);'
sql_creates['guests'] = 'CREATE TABLE IF NOT EXISTS guests(' \
                        'id INT AUTO_INCREMENT PRIMARY KEY,' \
                        'whoid INT NOT NULL, ' \
                        'whomid INT NOT NULL, ' \
                        'guest_date DATE NOT NULL,' \
                        'check_g BOOL NOT NULL DEFAULT FALSE);'
sql_creates['changes'] = 'CREATE TABLE IF NOT EXISTS changes(' \
                         'id INT AUTO_INCREMENT PRIMARY KEY,' \
                         'uid INT NOT NULL,' \
                         'reason INT NOT NULL,' \
                         'seed VARCHAR(1024) NOT NULL );'
sql_creates['confirmed'] = 'CREATE TABLE IF NOT EXISTS confirmed(' \
                           'uid INT NOT NULL UNIQUE,' \
                           'confirm_email bool DEFAULT FALSE,' \
                           'full_profile bool DEFAULT FALSE,' \
                           'photo_is_available bool DEFAULT FALSE);'
sql_creates['online'] = 'CREATE TABLE IF NOT EXISTS online(' \
                        'uid INT NOT NULL UNIQUE,' \
                        'time_until DATETIME NOT NULL);'
sql_creates['block'] = 'CREATE TABLE IF NOT EXISTS block(' \
                       'whoid INT NOT NULL,' \
                       'whomid INT NOT NULL);'

mydb = mysql.connector.connect(
    host="192.168.99.102",
    user="root",
    passwd="qwerty"
)

mycursor = mydb.cursor()
for key, query in sql_creates.items():
    mycursor.execute(query)
    print("%s execute success!" % key)
