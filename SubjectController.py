import random

from Subject import Subject
from Student import Student
from Database import Database

from Utils import MAX_ENROLLED_SUBJECTS

class SubjectController():
    def __init__(self, db: Database):
        self.db = db


    def _generate_id(self) -> str:
        """Generate a unique subject id.

        Returns:
            str: subject id
        """
        existing_ids = []
        for student in self.db.students:
            for subject in student.subjects:
                existing_ids.append(subject.id)

        unique = False
        while not unique:
            id = str(random.randint(0, 999)).zfill(3)
            unique = id not in existing_ids
        return id


    def _generate_mark(self) -> int:
        """Generate a random mark between 25 and 100.

        Returns:
            int: random mark
        """
        return random.randint(25, 100)


    def generate_subject(self) -> Subject:
        """Generate a subject object with a unique id and random mark.

        Returns:
            Subject: subject object
        """
        return Subject(self._generate_id(), self._generate_mark())


    def enrol_student(self, student: Student) -> bool:
        """Enrol a student into a new subject.
        Will also save results to db.
        Args:
            student (Student): Student to be encrolled

        Returns:
            bool: True if successful, False if exceeds maximum number of allowed subject enrollments
        """
        if len(student.subjects) < MAX_ENROLLED_SUBJECTS:
            student.subjects.append(self.generate_subject())
            self.db.upsert(student)
            return True

        else:
            return False


    def unenrol_student(self, student: Student, subject_id: str) -> bool:
        """Unenrol a passed student from a subject, pointed to by the subject_id.
        Will also save results to db.

        Args:
            student (Student): Student to unenrol
            subject_id (str): subject id

        Returns:
            bool: True if was successful, False if student is not enrolled to passed subject_id
        """
        for i, subject in enumerate(student.subjects):
            if subject.id == subject_id:
                student.subjects.pop(i)
                self.db.upsert(student)
                return True
        return False
