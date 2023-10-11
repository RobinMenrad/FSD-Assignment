import json
from Student import Student
from Subject import Subject
from Utils import *

class Database():
    def __init__(self, db_path):
        self.db_path = db_path
        self.students = []
        self._load()


    def _load(self):
        """Load from the db file a list of student objects"""
        self.students = [] # we load after any save to file to keep self.students consistent
        try:
            with open(self.db_path) as f:
                self.db = json.load(f)
                for student in self.db:
                    self.students.append(Student(
                        student['id'],
                        student['name'],
                        student['email'],
                        student['password'],
                        [Subject(subject['id'], subject['mark']) for subject in student['subjects']],
                    ))
        except FileNotFoundError:
            self.db = []


    def get_student(self, id: str) -> Student:
        """Get a student by the student id.

        Args:
            id (str): student id

        Returns:
            Student: Student object
        """
        for student in self.students:
            if student.id == id:
                return student
        return None


    def insert(self, student: Student):
        """Insert a new student into the database and save.

        Args:
            student (Student): Student to be added to db

        Raises:
            StudentAlreadyExistsException: If the student already exists in the db
        """
        if self.get_student(student.id):
            raise StudentAlreadyExistsException()
        self.db.append(dict(student))
        self.save()


    def upsert(self, student: Student):
        """Either update or insert a new student.

        Args:
            student (Student): Student object to update or insert to the databse
        """
        updated = False
        for i, db_student in enumerate(self.students):
            if student.id == db_student.id:
                self.db[i] = dict(student)
                updated = True
        if not updated:
            self.db.append(dict(student))
        self.save()


    def delete_student(self, student: Student):
        """Remove a student from the db.

        Args:
            student (Student): Student to be removed from the db
        """
        for i, db_student in enumerate(self.students):
            if student.id == db_student.id:
                self.db.pop(i)
                break
        self.save()


    def save(self):
        """save the db to file and reload it."""
        with open(self.db_path, 'w') as f:
            json.dump(self.db, f)
        self._load()
