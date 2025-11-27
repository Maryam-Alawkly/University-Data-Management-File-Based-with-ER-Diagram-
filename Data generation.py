import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import os

# Initialize Faker for Arabic data generation
fake = Faker('ar_SA')

# Define file names and column headers
FILES = {
    'departments': 'Department.csv',
    'students': 'Student.csv',
    'courses': 'Course.csv',
    'instructors': 'Instructor.csv',
    'enrollments': 'Enrollment.csv'
}

department_columns = ['DepartmentID', 'DepartmentName']
student_columns = ['StudentID', 'FirstName', 'LastName', 'DateOfBirth', 'Major', 'Address', 'Phone']
course_columns = ['CourseID', 'CourseName', 'Credits', 'Department']
instructor_columns = ['InstructorID', 'FirstName', 'LastName', 'Department', 'Rank', 'Email']
enrollment_columns = ['StudentID', 'CourseID', 'Semester', 'Year', 'Grade']

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

# ------ Data Generation Functions ------
def generate_departments(num):
    departments = []
    for i in range(num):
        dept_id = f"D{str(i+1).zfill(4)}"
        dept_name = fake.random_element([
            'كلية الصيدلة', 'كلية التربية', 'كلية العلوم',
            'كلية الهندسة', 'كلية الزراعة', 'كلية الطب'
        ])
        departments.append([dept_id, dept_name])
    return departments

def generate_students(num, departments):
    students = []
    dept_names = [d[1] for d in departments]
    
    for i in range(num):
        student_data = {
            'StudentID':  f"2025{str(i+1).zfill(4)}",
            'FirstName': fake.first_name(),
            'LastName': fake.last_name(),
            'DateOfBirth': fake.date_of_birth(minimum_age=17, maximum_age=25).strftime('%Y-%m-%d'),
            'Major': random.choice(dept_names),
            'Address': fake.random_element(elements=('القبة', 'المرج', 'البيضاء', 'بنغازي', 'طرابلس')),
            'Phone': fake.random_element(elements=([f"091{random.randint(1000000,9999999)}", f"092{random.randint(1000000,9999999)}"]))
        }
        
        try:
            _validate_not_null(student_data, ['StudentID', 'FirstName', 'LastName', 'DateOfBirth', 'Major'])
            _validate_dob(student_data['DateOfBirth'])
            students.append(list(student_data.values()))
        except Exception as e:
            print(f"Invalid data skipped {e}")
    return students

def generate_courses(num, departments):
    courses = []
    dept_names = [d[1] for d in departments]
    
    for i in range(num):
        course_data = {
            'CourseID': f"C{str(i+1).zfill(4)}",
            'CourseName': fake.random_element([
                'كتابة تقارير', 'مهارات تواصل', 'عربي',
                'انجليزي', 'رياضة', 'فيزياء', 'كيمياء'
            ]),
            'Credits': random.randint(1, 4),
            'Department': random.choice(dept_names)
        }
        
        try:
            _validate_credits(course_data['Credits'])
            courses.append(list(course_data.values()))
        except Exception as e:
            print(f"Invalid data skipped {e}")
    return courses

def generate_instructors(num, departments):
    instructors = []
    dept_names = [d[1] for d in departments]
    
    for i in range(num):
        instructor_data = {
            'InstructorID': f"I{str(i+1).zfill(4)}",
            'FirstName': fake.first_name(),
            'LastName': fake.last_name(),
            'Department': random.choice(dept_names),
            'Rank': fake.random_element(elements=('أستاذ', 'أستاذ مساعد', 'محاضر')),
            'Email': fake.unique.email()
        }
        
        try:
            _validate_unique('Email', instructor_data['Email'], FILES['instructors'])
            instructors.append(list(instructor_data.values()))
        except Exception as e:
            print(f"Invalid data skipped {e}")    
    return instructors

def generate_enrollments(students, courses):
    enrollments = []
    student_ids = [s[0] for s in students]
    course_ids = [c[0] for c in courses]
    
    for _ in range(len(students) * 2):
        enroll_data = {
            'StudentID': random.choice(student_ids),
            'CourseID': random.choice(course_ids),
            'Semester': random.choice(['الفصل الأول', 'الفصل الثاني']),
            'Year': random.randint(2020, 2023),
            'Grade': random.randint(50, 100)
        }
        
        enrollments.append(list(enroll_data.values()))
    return enrollments

def save_to_csv(data, columns, filename):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Created {filename} Successfully :)")


# ------ Main Implementation ------
def main():
    # Data generation and save to CSV files
    departments = generate_departments(6)
    students = generate_students(10000, departments)
    courses = generate_courses(10000, departments)    
    instructors = generate_instructors(10000, departments)
    enrollments = generate_enrollments(students, courses)

    save_to_csv(departments, department_columns, FILES['departments'])
    save_to_csv(students, student_columns, FILES['students'])
    save_to_csv(courses, course_columns, FILES['courses'])
    save_to_csv(instructors, instructor_columns, FILES['instructors'])
    save_to_csv(enrollments, enrollment_columns, FILES['enrollments'])
    print("Files created successfully :)")

if __name__ == "__main__":
    main()