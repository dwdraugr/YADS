from typing import List

import app.core.const_data as const_data
import re


class User:
    def __init__(self):
        self._id = 0
        self._email = 'bibi@example.com'
        self._nickname = 'bibonsky'
        self._first_name = 'Biba'
        self._last_name = 'Bobinsky'
        self._rating = 1337
        self._geo = "47'21:56'16"
        self._biography = "I'm test biography"
        self._tags = ['cinema', 'fishing', 'bbb']
        self._sex_pref = 'wood'
        self._gender = 'helicopter'
        self._age = 42
        self._pictures = ['sea', 'pig', 'goblin']

    @property
    def id(self):
        return self._id

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, val):
        if type(val) is int:
            self._rating = val
        else:
            raise TypeError('Value must be int')

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, val):
        if type(val) is int:
            if 18 < val < 128:
                self._age = val
            else:
                raise ValueError('Incorrect Age')
        else:
            raise TypeError('Value must be int')

    @property
    def nickname(self) -> str:
        return self._nickname

    @nickname.setter
    def nickname(self, val):
        if type(val) is str:
            if len(val) < 30:
                self._nickname = val
            else:
                raise ValueError('Too long nickname')
        else:
            raise TypeError('Value must be string')

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, val):
        if type(val) is str:
            if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", val):
                self._nickname = val
            else:
                raise ValueError('Incorrect e-mail')
        else:
            raise TypeError('Value must be string')

    @property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def first_name(self, val):
        if type(val) is str:
            if len(val) < 40:
                self._first_name = val
            else:
                raise ValueError('Too long first name')
        else:
            raise TypeError('Value must be string')

    @property
    def last_name(self) -> str:
        return self._last_name

    @last_name.setter
    def last_name(self, val):
        if type(val) is str:
            if len(val) < 45:
                self._last_name = val
            else:
                raise ValueError('Too long last name')
        else:
            raise TypeError('Value must be string')

    @property
    def biography(self) -> str:
        return self._biography

    @biography.setter
    def biography(self, val):
        if type(val) is str:
            if len(val) < 1000:
                self._biography = val
            else:
                raise ValueError('Too long biography')
        else:
            raise TypeError('Value must be string')

    @property
    def sex_pref(self) -> str:
        return self._sex_pref

    @sex_pref.setter
    def sex_pref(self, val):
        if type(val) is str:
            if val in const_data.sex_preferences:
                self._sex_pref = val
            else:
                raise ValueError('This sex preference has not yet been invented')
        else:
            raise TypeError('Value must be string')

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, val):
        if type(val) is str:
            if val in const_data.genders:
                self._sex_pref = val
            else:
                raise ValueError('This gender has not yet been invented')
        else:
            raise TypeError('Value must be string')

    @property
    def tags(self) -> List:
        return self._tags

    def append_tag(self, new_tag):
        if type(new_tag) is str:
            if new_tag in const_data.tags:
                self._tags.append(new_tag)
            else:
                raise ValueError('Tag not exist')
        else:
            raise TypeError('Value must be string')

    def remove_tag(self, removed_tag):
        if type(removed_tag) is str:
            if removed_tag in self._tags:
                self._tags.remove(removed_tag)
            else:
                raise ValueError('User does not have this tag')
        else:
            raise TypeError('Value must be string')

    @property
    def pictures(self) -> List:
        return self.pictures

    def append_picture(self, new_pic):
        if type(new_pic) is str:
            self._tags.append(new_pic)
        else:
            raise TypeError('Value must be string')

    def get_picture(self, pic):
        if type(pic) is str:
            if pic in self._pictures:
                return pic  # TODO: must return IMG
            else:
                raise ValueError('User does not have this picture')
        else:
            raise TypeError('Value must be string')

    def remove_picture(self, removed_pic):
        if type(removed_pic) is str:
            if removed_pic in self._pictures:
                self._tags.remove(removed_pic)
            else:
                raise ValueError('User does not have this picture')
        else:
            raise TypeError('Value must be string')

if __name__ == '__main__':
    a = User()
    print(hasattr(a, 'age'))
    print(hasattr(a, 'bibos'))
