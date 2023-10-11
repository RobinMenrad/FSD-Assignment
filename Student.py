from Subject import Subject
from Utils import mark_to_grade

class Student():
    def __init__(self, id: str, name: str, email: str, password: str, subjects: list[Subject]):
        self.id = id
        self.subjects = subjects
        self.password = password
        self.name = name
        self.email = email

    def get_average_mark(self) -> int:
        """Get the average mark of the given student.

        Returns:
            int: average student mark
        """
        # Return -1 if student not enrolled in any subjects
        if len(self.subjects) == 0:
            return -1
        grades = [subject.mark for subject in self.subjects]
        return sum(grades)/len(grades)


    def get_grade(self) -> str:
        """Get the grade of the student based off the students average mark.

        Returns:
            str: students mark
        """
        return mark_to_grade(self.get_average_mark())


    def is_pass(self) -> bool:
        """Whether the student is a pass or fail.

        Returns:
            bool: True if pass, False if fail
        """
        if self.get_average_mark() >= 50:
            return True
        return False


    def __iter__(self):
        for key in self.__dict__:
            if key == 'subjects':
                yield key, [dict(subject) for subject in self.subjects]
            else:
                yield key, getattr(self, key)


    def __str__(self):
        return f"{self.name} :: {self.id} --> Email: {self.email}"
