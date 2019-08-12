import unittest
import app.core.user as app


class MyTest(unittest.TestCase):
    def test_age(self):
        test = app.User()
        self.assertEqual(test.age, 42)

    def test_biography(self):
        self.assertEqual(app.User().biography,
                         "I'm test biography")

    def test_sex_pref(self):
        self.assertEqual(app.User().sex_pref,
                         "wood")

    def test_gender(self):
        self.assertEqual(app.User().gender,
                         "helicopter")

    def test_pictures(self):
        self.assertEqual(app.User().pictures,
                         ['sea', 'pig', 'goblin'])

    def test_tags(self):
        self.assertEqual(app.User().tags,
                         ['cinema', 'fishing', 'bbb'])



if __name__ == '__main__':
    lal = app.User()
    print(type(lal.age))
    unittest.main()
