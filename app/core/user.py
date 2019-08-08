from typing import List


class User:
    age: int
    biography: str
    sex_pref: str
    gender: str
    pictures: List[str]
    tags: List[str]
    geo: List[str]

    def __init__(self):
        self.biography = "I'm test biography"
        self.tags = ['cinema', 'fishing', 'bbb']
        self.sex_pref = 'wood'
        self.gender = 'helicopter'
        self.age = 42
        self.pictures = ['sea', 'pig', 'goblin']


