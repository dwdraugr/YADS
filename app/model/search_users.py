from flask import Flask
import mysql.connector.errors as error
from app.model.model import Model, all_tags


class SearchUser(Model):
    def __init__(self):
        super(SearchUser, self).__init__()
        self.cursor = self.matchadb.cursor()

    def preferences(self, user):
        data = set()
        data.update(self.search_by_tags(user['tags']))
        data.update(self.search_by_geo(user['city'], user['region'],
                                       user['country']))
        data.update(self.search_by_age(0, 200))
        data.update(self.search_by_rating(0, 4000000))
        data &= set(self.search_by_gender(user['sex_pref']))
        data -= self.search_by_block(user['id'])
        return data

    def search(self, tags: tuple = None, geo: tuple = None, min_age: int = None,
               max_age: int = None, min_rating: int = None,
               max_rating: int = None, sex_pref: str = None):
        data = set()
        if 0 != len(tags):
            result = self.search_by_tags(tags)
            data.update(set(result))
        else:
            result = self.search_by_tags(all_tags)
            data.update(set(result))
        if geo is not None:
            result = self.search_by_geo(geo[0], geo[1], geo[2])
            if len(result) == 0:
                data.update(set(result))
            else:
                data &= set(result)
        if min_age and max_age is not None:
            result = self.search_by_age(min_age, max_age)
            if len(result) == 0:
                data.update(set(result))
            else:
                data &= set(result)
        if min_rating and max_rating is not None:
            result = self.search_by_rating(min_rating, max_rating)
            if len(result) == 0:
                data.update(set(result))
            else:
                data &= set(result)
        if sex_pref is not None:
            result = self.search_by_gender(sex_pref)
            if len(result) == 0:
                data.update(set(result))
            else:
                data &= set(result)
        return list(data)

    def search_by_tags(self, tags: tuple):
        result = []
        for tag in tags:
            result.extend(self.search_by_tag(tag))
        return list(set(result))

    def search_by_tag(self, tag_name):
        self.cursor.execute("SELECT uid FROM tags WHERE tag = %s", (tag_name,))
        if self.cursor.rowcount != 0:
            return [item[0] for item in self.cursor.fetchall()]
        else:
            return None

    def search_by_geo(self, country=None, region=None, city=None):
        if country == region == city is None:
            return None
        if city is not None:
            self.cursor.execute('SELECT uid FROM geo WHERE city = %s', (city,))
            if self.cursor.rowcount != 0:
                return [item[0] for item in self.cursor.fetchall()]
        elif region is not None:
            self.cursor.execute('SELECT uid FROM geo WHERE city = %s',
                                (region,))
            if self.cursor.rowcount != 0:
                return [item[0] for item in self.cursor.fetchall()]
        elif country is not None:
            self.cursor.execute('SELECT uid FROM geo WHERE city = %s',
                                (country,))
            if self.cursor.rowcount != 0:
                return [item[0] for item in self.cursor.fetchall()]
        return None

    def search_by_age(self, min_age, max_age):
        self.cursor.execute("SELECT uid FROM options WHERE YEAR(age) >= YEAR(DATE_SUB(NOW(), INTERVAL %s YEAR )) AND YEAR(age) <= YEAR(DATE_SUB(NOW(), INTERVAL %s YEAR ))",
                            (max_age, min_age))
        if self.cursor.rowcount != 0:
            return [item[0] for item in self.cursor.fetchall()]
        else:
            return None

    def search_by_rating(self, min_rating, max_rating):
        self.cursor.execute("SELECT uid FROM ratings WHERE rating >= %s AND "
                            "rating <= %s",
                            (min_rating, max_rating))
        if self.cursor.rowcount != 0:
            return [item[0] for item in self.cursor.fetchall()]
        else:
            return None

    def search_by_gender(self, sex_pref):
        if sex_pref == 'Male' or sex_pref == 'Female':
            self.cursor.execute("SELECT uid FROM options WHERE gender = %s",
                                (sex_pref,))
        else:
            self.cursor.execute("SELECT uid FROM options")
        if self.cursor.rowcount != 0:
            return [item[0] for item in self.cursor.fetchall()]
        else:
            return None

    def search_by_block(self, uid):
        self.cursor.execute('SELECT whomid FROM block WHERE whoid = %s', (uid,))
        return set([item[0] for item in self.cursor.fetchall()])
