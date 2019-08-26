import mysql.connector as sql
import requests

from app.model.model import Model


class CollectInfo(Model):
    def collect_all(self, data: dict):
        self._collect_names(data['uid'], data['first'], data['last'])
        self._collect_options(data['uid'], data['gender'],
                              data['sex_pref'], data['age'])
        self._collect_biography(data['uid'], data['biography'])
        self._collect_geo_ip(data['uid'], data['ip'])
        self._collect_tags(data['uid'], data['tags'])
        self._create_rating(data['uid'])

    def _collect_names(self, uid, first, last):
        cursor = self.matchadb.cursor()
        cursor.execute("INSERT INTO names (uid, first_name, last_name)"
                       "VALUES (%s, %s, %s)", (uid, first, last))
        if cursor.rowcount == 0:
            raise sql.errors.Error('Unable to write in database')

    def _collect_options(self, uid, gender, sex_pref, age):
        cursor = self.matchadb.cursor(dictionary=True)
        cursor.execute("INSERT INTO options (uid, gender, sex_pref, age)"
                       "VALUES (%s, %s, %s, %s)", (uid, gender, sex_pref, age))
        if cursor.rowcount == 0:
            raise sql.errors.Error('Unable to write in database')

    def _collect_biography(self, uid, biography):
        cursor = self.matchadb.cursor()
        cursor.execute("INSERT INTO biographies (uid, biography)"
                       "VALUES (%s, %s)", (uid, biography))
        if cursor.rowcount == 0:
            raise sql.errors.Error('Unable to write in database')

    def _collect_geo_ip(self, uid, ip): # TODO: Fix TypeError with try
        request_str = self._get_geo_address(ip)
        response = requests.get(request_str)
        json = response.json()
        if json is not None:
            cursor = self.matchadb.cursor()
            print(json)
            cursor.execute("INSERT INTO geo "
                           "(uid, country, region, city, gps_geo)"
                           "VALUES (%s, %s, %s, %s, %s)",
                           (uid, json['country_name'], json['region_name'],
                            json['city'],
                            json['latitude'] + ';' + json['longitude']))
            if cursor.rowcount == 0:
                raise sql.errors.Error('Unable to write in database')
        else:
            raise requests.HTTPError('Unable to connect to some server')

    def _create_rating(self, uid):
        cursor = self.matchadb.cursor()
        cursor.execute("INSERT INTO ratings (uid, rating)"
                       "VALUES (%s, 0)", (uid,))
        if cursor.rowcount == 0:
            raise sql.errors.Error('Unable to write in database')

    def _collect_tags(self, uid, tags: list):
        cursor = self.matchadb.cursor()
        for tag in tags:
            cursor.execute("INSERT INTO tags (uid, tag)"
                           "VALUES (%s, %s)", (uid, tag))
            if cursor.rowcount == 0:
                raise sql.errors.Error('Unable to write in database')
