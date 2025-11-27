import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import os

# Define file names and column headers
FILES = {
    'departments': 'Department.csv',
    'students': 'Student.csv',
    'courses': 'Course.csv',
    'instructors': 'Instructor.csv',
    'enrollments': 'Enrollment.csv'
}

# ------ Validation Functions ------
def _validate_not_null(data, required_fields):
    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"{field} Its empty!")

def _validate_unique(field, value, file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if value in df[field].values:
            raise ValueError(f" {value} Already exists{field}")

def _validate_credits(credits):
    if not 1 <= credits <= 4:
        raise ValueError("The hours must be between 1 and 4 ")

def _validate_dob(dob_str):
    dob = datetime.strptime(dob_str, '%Y-%m-%d')
    if dob > datetime.now() - timedelta(days=365*17):
        raise ValueError("The age must be greater than 17")
    
def _validate_grade(grade):
    if not 0 <= grade <= 100:
        raise ValueError("The grade must be between 0 and 100 ")

# ------ Referential Integrity Functions ------
def _delete_related_records(main_file, related_file, key_field, key_value):
    if os.path.exists(related_file):
        df = pd.read_csv(related_file)
        df = df[df[key_field] != key_value]
        df.to_csv(related_file, index=False, encoding='utf-8-sig')

def _update_related_ids(file_path, id_field, old_id, new_id):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df.loc[df[id_field] == old_id, id_field] = new_id
        df.to_csv(file_path, index=False, encoding='utf-8-sig')

# ------ Data Retrieval ------
def retrieve_student(student_id):
    if os.path.exists(FILES['students']):
        df = pd.read_csv(FILES['students'])
        student_data = df[df['StudentID'] == student_id]
        if not student_data.empty:
            print("Student Data :")
            print(student_data.to_string(index = False))
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def retrieve_courses_by_department(department_name):
    if os.path.exists(FILES['courses']):
        df = pd.read_csv(FILES['courses'])
        department_data = df[df['Department'] == department_name]
        if not department_data.empty:
                print("Department Data :")
                print(department_data.to_string(index = False))
        else:
                print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def retrieve_students_in_course(course_id):
    if os.path.exists(FILES['enrollments']):
        df = pd.read_csv(FILES['enrollments'])
        student_ids = df[df['CourseID'] == course_id]['StudentID']
        if not student_ids.empty:
            print("Student Data :")
            print(student_ids.to_string(index = False))
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def retrieve_instructor(instructor_id):
    if os.path.exists(FILES['instructors']):
        df = pd.read_csv(FILES['instructors'])
        instructor_data = df[df['InstructorID'] == instructor_id]
        if not instructor_data.empty:
            print("Instructor Data :")
            print(instructor_data.to_string(index = False))
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def retrieve_enrollments_for_student(student_id):
    if os.path.exists(FILES['enrollments']):
        df = pd.read_csv(FILES['enrollments'])
        student_data = df[df['StudentID'] == student_id]
        if not student_data.empty:
            print("Student Data :")
            print(student_data.to_string(index = False))
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def retrieve_average_grade(course_id, semester):
    if os.path.exists(FILES['enrollments']):
        df = pd.read_csv(FILES['enrollments'])
        grades = df[(df['CourseID'] == course_id) & (df['Semester'] == semester)]['Grade']        
        if not grades.empty:
            print(grades.mean())
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

# ------ Main Implementation ------
def main():
    retrieve_student(20254100)
    retrieve_courses_by_department('كلية الهندسة')
    retrieve_students_in_course('C0004')
    retrieve_instructor('I0004')
    retrieve_enrollments_for_student(20250040)
    retrieve_average_grade('C0004', 'الفصل الثاني')

if __name__ == "__main__":
    main()