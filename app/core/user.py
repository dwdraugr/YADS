from typing import List


class User:
    age: int
    biography: str
    sex_pref: str
    gender: str
    pictures: List[str]
    tags: List[str]

    def __init__(self):
        self.biography = "I'm test biography"
        self.tags = ['cinema', 'fishing', 'разведопросы']
        self.sex_pref = 'wood'
        self.gender = 'helicopter'
        self.age = 42
        self.pictures = ['sea', 'pig', 'goblin']

    @property
    def age(self) -> int:
        return self.age

    @age.setter
    def age(self, value: int):
        if value < 16:
            return
        elif value > 122:
            return  # TODO: Add throw
        else:
            self.age = value

    @property
    def gender(self) -> str:
        return self.gender

    @gender.setter
    def gender(self, value: str):
        if value != 'male' or value != 'female':
            return  # TODO: Add throw
        else:
            self.gender = value

    @property
    def sex_pref(self) -> str:
        return self.gender

    @sex_pref.setter
    def sex_pref(self, value: str):
        if value != 'male' or value != 'female' or value != 'bisexual':
            return  # TODO: Add throw
        else:
            self.sex_pref = value

    @property
    def biography(self) -> str:
        return self.biography

    @biography.setter
    def biography(self, value: str):
        if len(value) > 500:
            self.biography = len[:500]



