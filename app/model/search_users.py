from app.model.model import Model


class SearchUser(Model):
    def search_by_tag(self, tag_name):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT uid FROM tags WHERE tag = %s", (tag_name,))
        users = [item[0] for item in cursor.fetchall()]
        return users

    def search_by_geo(self, country=None, region=None, city=None):
        if country == region == city is None:
            return None
        cursor = self.matchadb.cursor()
        city_users = []
        region_users = []
        country_users = []
        if city is not None:
            cursor.execute('SELECT uid FROM geo WHERE city = %s', (city,))
            if cursor.rowcount != 0:
                city_users = [item[0] for item in cursor.fetchall()]
        if region is not None:
            cursor.execute('SELECT uid FROM geo WHERE city = %s', (region,))
            if cursor.rowcount != 0:
                region_users = [item[0] for item in cursor.fetchall()]
        if country is not None:
            cursor.execute('SELECT uid FROM geo WHERE city = %s', (country,))
            if cursor.rowcount != 0:
                country_users = [item[0] for item in cursor.fetchall()]
        data = list(set(city_users + region_users + country_users))
        return data

    def search_by_age(self, min_age, max_age):
        cursor = self.matchadb.cursor()
        cursor.execute("SELECT uid FROM options WHERE age >= %s AND age <= %s",
                       (min_age, max_age))
        if cursor.rowcount != 0:
            return [item[0] for item in cursor.fetchall()]
        else:
            return None
