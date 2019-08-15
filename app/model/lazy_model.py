import mysql.connector


class lazy_model():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="192.168.99.100",
            user="root",
            passwd="qwerty",
            database='matcha'
        )

    def get_all(self, id):
        self.mycursor.execute()

    def get_age(self, id):
        self.mycursor.execute("SELECT age from ")

    def get_gender(self):
        return {'gender': 'male'}

    def get_sex_pref(self):
        return {'sex_pref': 'helicopter'}

    def get_biography(self):
        return {'biography': "I'm coil"}

    def get_tags(self):
        return {
            'tags':
                [
                    'beer',
                    'oil',
                    'gasoline'
                ]
        }

    def get_photos(self):
        return {
            'photos':
                [
                    'one',
                    'two',
                    'tri'
                ]
        }
