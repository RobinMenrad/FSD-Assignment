from Utils import mark_to_grade

class Subject():
    def __init__(self, id: int, mark: int):
        self.id = id
        self.mark = mark

    def __iter__(self):
        for key in self.__dict__:
            yield key, getattr(self, key)

    def __str__(self):
        return f"[ Subject::{self.id} -- mark = {self.mark} -- grade = {mark_to_grade(self.mark)} ]"
