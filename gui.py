import tkinter as tk
from tkinter import messagebox
import json

class GUIUniApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUIUniApp - Student Login")
        self.root.geometry("400x400")

        self.login_frame = tk.Frame(self.root, padx=20, pady=20)
        self.login_frame.pack()

        self.email_label = tk.Label(self.login_frame, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.login_frame, width=30)
        self.email_entry.pack(pady=10)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self.login_frame, show="*", width=30)
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, width=10, height=2, bg="blue", fg="white")
        self.login_button.pack(pady=10)

        self.enrollment_frame = None
        self.subjects_frame = None

        self.student_data = []  # Initialize an empty list for student data.

        # Read student data from the "students.data" file (assumed to be in JSON format).
        try:
            with open("students.data", "r") as file:
                self.student_data = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "Students data file not found")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error decoding JSON data")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        for student in self.student_data:
            if student.get("email") == email and student.get("password") == password:
                self.login_frame.destroy()
                self.enrollment_window()
                break
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def enrollment_window(self):
        self.enrollment_frame = tk.Frame(self.root, padx=20, pady=20)
        self.enrollment_frame.pack()

        self.enrollment_label = tk.Label(self.enrollment_frame, text="Enroll in Subjects", font=("Helvetica", 16))
        self.enrollment_label.pack(pady=10)

        self.subjects = ["Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5", "Subject 6"]
        self.selected_subjects = []

        for subject in self.subjects:
            subject_checkbox = tk.Checkbutton(self.enrollment_frame, text=subject, command=lambda subj=subject: self.update_subjects(subj))
            subject_checkbox.pack(anchor="w", padx=10)

        self.enroll_button = tk.Button(self.enrollment_frame, text="Enroll", command=self.show_enrolled_subjects, width=10, height=2, bg="blue", fg="white")
        self.enroll_button.pack(pady=10)

    def update_subjects(self, subject):
        if subject in self.selected_subjects:
            self.selected_subjects.remove(subject)
        else:
            self.selected_subjects.append(subject)

    def show_enrolled_subjects(self):
        if len(self.selected_subjects) > 4:
            self.error_window("Maximum 4 subjects allowed.")
        else:
            if self.enrollment_frame:
                self.enrollment_frame.destroy()
            if self.subjects_frame:
                self.subjects_frame.destroy()

            self.subjects_frame = tk.Frame(self.root, padx=20, pady=20)
            self.subjects_frame.pack()

            subjects_label = tk.Label(self.subjects_frame, text="Enrolled Subjects", font=("Helvetica", 16))
            subjects_label.pack(pady=10)

            subject_text = "\n".join(self.selected_subjects)
            subject_label = tk.Label(self.subjects_frame, text=subject_text)
            subject_label.pack()

    def error_window(self, message):
        error_frame = tk.Toplevel(self.root)
        error_frame.title("Error")
        error_frame.geometry("300x100")

        error_label = tk.Label(error_frame, text=message, fg="red")
        error_label.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIUniApp(root)
    root.mainloop()
