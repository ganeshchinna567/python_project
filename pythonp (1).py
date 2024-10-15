class Student:
    def __init__(self, name, roll_number):
        self.name = name
        self.roll_number = roll_number
        self.grades = {}

    def add_grade(self, subject, grade):
        if 0 <= grade <= 100:
            self.grades[subject] = grade
        else:
            print("Invalid grade. Please enter a grade between 0 and 100.")

    def calculate_average(self):
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Roll Number: {self.roll_number}")
        print("Grades:")
        for subject, grade in self.grades.items():
            print(f"  {subject}: {grade}")
        print(f"Average Grade: {self.calculate_average():.2f}")
class StudentTracker:
    def __init__(self):
        self.students = {}

    def add_student(self, name, roll_number):
        if roll_number not in self.students:
            self.students[roll_number] = Student(name, roll_number)
        else:
            print("Student with this roll number already exists.")

    def add_grades(self, roll_number, subject, grade):
        if roll_number in self.students:
            self.students[roll_number].add_grade(subject, grade)
        else:
            print("Student not found.")

    def view_student_details(self, roll_number):
        if roll_number in self.students:
            self.students[roll_number].display_info()
        else:
            print("Student not found.")

    def calculate_average(self, roll_number):
        if roll_number in self.students:
            return self.students[roll_number].calculate_average()
        else:
            print("Student not found.")
            return 0
def add_student_ui(tracker):
    name = input("Enter student name: ")
    roll_number = input("Enter roll number: ")
    tracker.add_student(name, roll_number)

def add_grades_ui(tracker):
    roll_number = input("Enter roll number: ")
    subject = input("Enter subject: ")
    grade = float(input("Enter grade: "))
    tracker.add_grades(roll_number, subject, grade)

def view_student_details_ui(tracker):
    roll_number = input("Enter roll number: ")
    tracker.view_student_details(roll_number)

def calculate_average_ui(tracker):
    roll_number = input("Enter roll number: ")
    average = tracker.calculate_average(roll_number)
    print(f"Average Grade: {average:.2f}")
def main():
    tracker = StudentTracker()
    while True:
        print("1. Add Student")
        print("2. Add Grades")
        print("3. View Student Details")
        print("4. Calculate Average Grades")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            add_student_ui(tracker)
        elif choice == '2':
            add_grades_ui(tracker)
        elif choice == '3':
            view_student_details_ui(tracker)
        elif choice == '4':
            calculate_average_ui(tracker)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    
import sqlite3
class StudentTracker:
    def __init__(self, db_name="students.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    roll_number TEXT PRIMARY KEY,
                    name TEXT
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS grades (
                    roll_number TEXT,
                    subject TEXT,
                    grade REAL,
                    FOREIGN KEY (roll_number) REFERENCES students (roll_number)
                )
            """)

    def add_student(self, name, roll_number):
        with self.conn:
            self.conn.execute("INSERT INTO students (roll_number, name) VALUES (?, ?)", (roll_number, name))

    def add_grades(self, roll_number, subject, grade):
        with self.conn:
            self.conn.execute("INSERT INTO grades (roll_number, subject, grade) VALUES (?, ?, ?)", (roll_number, subject, grade))

    def view_student_details(self, roll_number):
        student = self.conn.execute("SELECT name FROM students WHERE roll_number = ?", (roll_number,)).fetchone()
        if student:
            print(f"Name: {student[0]}")
            print(f"Roll Number: {roll_number}")
            grades = self.conn.execute("SELECT subject, grade FROM grades WHERE roll_number = ?", (roll_number,)).fetchall()
            print("Grades:")
            for subject, grade in grades:
                print(f"  {subject}: {grade}")
            average = self.calculate_average(roll_number)
            print(f"Average Grade: {average:.2f}")
        else:
            print("Student not found.")

    def calculate_average(self, roll_number):
        grades = self.conn.execute("SELECT grade FROM grades WHERE roll_number = ?", (roll_number,)).fetchall()
        if grades:
            return sum(grade[0] for grade in grades) / len(grades)
        return 0

