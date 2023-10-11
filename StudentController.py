import random
from collections import defaultdict
from typing import Union

from Student import Student
from Database import Database
from Subject import Subject
from SubjectController import SubjectController

from Utils import *


class StudentController():
    def __init__(self, db: Database, subject_controller: SubjectController):
        self.db = db
        self.subject_controller = subject_controller

        self.logged_in_student = None # once student is logged in, used to store student object


    def _generate_id(self) -> str:
        """Generate a unique student id.

        Returns:
            str: student id.
        """
        existing_ids = [student.id for student in self.db.students]
        unique = False
        while not unique:
            id = str(random.randint(0, 999999)).zfill(6)
            unique = id not in existing_ids
        return id


    def _email_name_lookup(self, email: str) -> Union[str, bool]:
        """For a given student email, return the student name.

        Args:
            email (str): studnet email

        Returns:
            Union[str, bool]: student name if known email, False if not a recognised email.
        """
        for student in self.db.students:
            if student.email == email:
                return student.name
        return False


    def _email_password_validate(self, email: str, password: str) -> Union[str, bool]:
        """assert email and password match for a user

        Args:
            email (str): student email.
            password (str): student password.

        Returns:
            Union[str, bool]: User id if match, False if not a match.
        """
        for student in self.db.students:
            if student.email == email and student.password == password:
                return student.id
        return False # used as an invalid id


    def register_student(self, email: str, password: str, name: str) -> str:
        """Register a new student with passed params and a new unique id.

        Args:
            email (str): student email.
            password (str): student password
            name (str): student name

        Returns:
            str: the new student_id
        """
        self.db.insert(Student(self._generate_id(), name, email, password, []))
        return id


    def group_students(self) -> dict:
        """Group students in fail, pass, credit, distinction, high distiction.

        Returns:
            dict: resultant grouping with grade as key and list of student_id's as value. i.e.
            {
                "P": ["001", "002"],
                "HD": ["003"]
            }
        """
        grades = defaultdict(list)
        for student in self.db.students:
            grade = student.get_grade()
            grades[grade].append(student.id)
        return dict(sorted(grades.items(), key = lambda x: GRADE_ORDERING.get(x[0], float('inf'))))


    def partition_students(self) -> dict:
        """Partition students into pass and fail.

        Returns:
            dict: resultant grouping with pass/fail as key and student id's as value. i.e.
            {
                "PASS": ["001", "002"],
                "FAIL": ["003"]
            }
        """
        partition = {'PASS': [], 'FAIL': []}
        for student in self.db.students:
            if student.is_pass():
                partition['PASS'].append(student.id)
            else:
                partition['FAIL'].append(student.id)
        return partition


    #### STUDENT MENU STUFF ###
    def student_course_menu(self):
        """Student course menu (Only allowed after login)
        Handels:
        - Change passsword
        - Enrol subject
        - Remove subject from enrolment
        - show enrolled subjects
        """
        exit = False
        while not exit:
            student_option = input_cyan('Student Course Menu (c/e/r/s/x): ', 2)

            # TODO i also added some logic around checking password format. Not sure if this is needed.
            if student_option == 'c': #change password
                print_yellow('Updating Password', 2)
                new_password = input_white('New Password: ', 2)
                confirmed_password = ''
                valid_password = False
                while (new_password != confirmed_password) and not valid_password:
                    confirmed_password = input_white('Confirm Password: ', 2)
                    if confirmed_password != new_password:
                        print_red('Password does not match - try again', 2)
                    if not password_check(new_password):
                        print_red('Incorrect password format', 2)

                self.logged_in_student.password = new_password
                self.db.upsert(self.logged_in_student)

            elif student_option == 'e': # enrol subject
                if self.subject_controller.enrol_student(self.logged_in_student):
                    print_yellow(f"Enrolling in Subject-{self.logged_in_student.subjects[-1].id}", 2)
                    print_yellow(f"You are now enrolled in {len(self.logged_in_student.subjects)} of {MAX_ENROLLED_SUBJECTS} subjects", 2)
                else:
                    print_red("Students are allowed to enrol in {MAX_ENROLLED_SUBJECTS} subjects only", 2)

            elif student_option == 'r': # remove subject from enrolment
                subject_id = input_white("Remove Subject by ID: ", 2)
                if self.subject_controller.unenrol_student(self.logged_in_student, subject_id):
                    print_yellow(f"Dropping Subject-{subject_id}", 2)
                    print_yellow(f"You are now enrolled in {len(self.logged_in_student.subjects)} out of {MAX_ENROLLED_SUBJECTS} subjects", 2)
                else:
                    print_yellow(f"You are not enrolled into subject-{subject_id}", 2)

            elif student_option == 's': # show encrolled subjects
                print_yellow(f"Showing {len(self.logged_in_student.subjects)} subjects", 2)
                for subject in self.logged_in_student.subjects:
                    print_white(subject, 2)

            elif student_option == 'x': # exit
                self.logged_in_student = None
                exit = True

            else:
                print_white('Invalid Input', 2)


    def student_login_menu(self):
        """Student login menu
        Handels:
        - Login student
        - Register student
        """
        exit = False
        while not exit:
            student_option = input_cyan('Student System (l/r/x) : ')

            if student_option == 'l': # login
                logged_in_id = self.login_student_sub_menu()
                if logged_in_id:
                    self.logged_in_student = self.db.get_student(logged_in_id)
                    self.student_course_menu()

            elif student_option == 'r': # register
                self.register_student_sub_menu()

            elif student_option == 'x': # exit
                exit = True

            else:
                print_white('Invalid Input')


    def login_student_sub_menu(self) -> Union[str, bool]:
        """Login student sub menu
        Handles student sign in.

        Returns:
            Union[str, bool]: logged in student id or False if unsuccessful login.
        """
        print_green('Student Sign In')

        correct_password = False
        while not correct_password:
            email = input_white('Email: ')
            password = input_white('Password: ')
            if not email_check(email) or not password_check(password):
                print_red("Incorrect email or password format")
            else:
                print_yellow("email and password formats acceptable")
                correct_password = True

        return self._email_password_validate(email, password)


    def register_student_sub_menu(self):
        """Student registration sub menu
        Handles Student registration.
        """
        print_green("Student Sign Up")

        correct_password = False
        while not correct_password:
            email = input_white("Email: ")
            password = input_white("Password: ")

            if not email_check(email) or not password_check(password):
                print_red("Incorrect email or password format")
            else:
                print_yellow("email and password formats acceptable")
                correct_password = True


        if email in [student.email for student in self.db.students]:
            print_red(f'Student {self._email_name_lookup(email)} already exists')
            return

        name = input_white("Name: ")
        print_yellow(f"Enrolling student {name}")
        self.register_student(email, password, name)
