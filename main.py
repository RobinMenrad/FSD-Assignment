from Database import Database
from StudentController import StudentController
from SubjectController import SubjectController
from Utils import *

db = Database('./students.data')
sub_c = SubjectController(db)
stu_c = StudentController(db, sub_c)

def admin_menu():
    exit = False
    while not exit:
        admin_option = input_cyan('Admin System (c/g/p/r/s/x) : ')

        if admin_option == 'c': # clear
            print_yellow("Clearing students database")
            clear = input_red("Are you sure you want to clear the database (Y)ES/(N)O: ")
            if clear == "Y":
                for student in db.students:
                    db.delete_student(student)
                print_yellow("Students data cleared")

        elif admin_option == 'g': # group students
            print_yellow("Grade Grouping")
            if len(db.students) == 0:
                print_white(" < Nothing to Display >", 2)
            else:
                grouping = stu_c.group_students()
                for grade in grouping.keys():
                    student_strings = f"{grade} --> ["
                    for student_id in grouping[grade]:
                        student = db.get_student(student_id)
                        student_strings += f"{student.name} :: {student.id} --> GRADE:  {grade} - MARK: {student.get_average_mark()}, "

                    print_white(student_strings.rstrip(', ') + "]")

        elif admin_option == 'p': # partition students
            print_yellow("PASS/FAIL Partition")
            paritions = stu_c.partition_students()
            for partition in paritions.keys():
                student_strings = f"{partition} --> ["
                for student_id in paritions[partition]:
                    student = db.get_student(student_id)
                    student_strings += f"{student.name} :: {student.id} --> GRADE:  {student.get_grade()} - MARK: {student.get_average_mark()}, "
                print_white(student_strings.rstrip(', ') + "]")

        elif admin_option == 'r': # remove students
            student_id = input_white('Remove by ID: ')
            if student_id not in [student.id for student in db.students]:
                print_red(f'Student {student_id} does not exist')
            else:
                print_yellow(f"Removing Student {student_id} Account")
                db.delete_student(db.get_student(student_id))

        elif admin_option == 's': # show students
            print_yellow("Student List")
            if len(db.students) == 0:
                print_white(" < Nothing to Display >", 2)
            for student in db.students:
                print_white(student)

        elif admin_option == 'x': # exit
            exit = True


if __name__ == '__main__':
    exit = False
    while not exit:
        uni_system_option = input_cyan('University System: (A)dmin, (S)tudent, or X : ', 0)

        if uni_system_option == 'A':
            admin_menu()

        elif uni_system_option == 'S':
            stu_c.student_login_menu()

        elif uni_system_option == 'X':
            print_yellow('Thank You', 0)
            exit = True
