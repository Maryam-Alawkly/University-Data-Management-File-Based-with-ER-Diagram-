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
            raise ValueError(f" {value} Already exists {field}")

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

# ------ Data Querying ------

# ------ Add New Records ------
def add_student(student_data):
    try:
        _validate_unique('StudentID', student_data['StudentID'], FILES['students'])
        _validate_not_null(student_data, ['StudentID', 'FirstName', 'LastName', 'DateOfBirth', 'Major'])
        _validate_dob(student_data['DateOfBirth'])
        students = pd.read_csv(FILES['students'])
        students = pd.concat([students, pd.DataFrame([student_data])], ignore_index=True)
        students.to_csv(FILES['students'], index=False, encoding='utf-8-sig')
        print(f"The record has been added :)")
            
    except Exception as e:
        print(f"An error occurred while adding the record{e}")

def add_course(course_data):
    try:
        _validate_unique('CourseID', course_data['CourseID'], FILES['courses'])
        _validate_not_null(course_data, ['CourseID','CourseName','Credits','Department'])
        _validate_credits(course_data['Credits'])
        courses = pd.read_csv(FILES['courses'])
        courses = pd.concat([courses, pd.DataFrame([course_data])], ignore_index=True)
        courses.to_csv(FILES['courses'], index=False, encoding='utf-8-sig')
        print(f"The record has been added :)")
    except Exception as e:
        print(f"An error occurred while adding the record{e}")

def add_instructor(instructor_data):
    try:
        _validate_unique('InstructorID', instructor_data['InstructorID'], FILES['instructors'])
        _validate_not_null(instructor_data, ['InstructorID','FirstName','LastName','Department'])
        _validate_unique('Email', instructor_data['Email'], FILES['instructors'])
        instructors = pd.read_csv(FILES['instructors'])
        instructors = pd.concat([instructors, pd.DataFrame([instructor_data])], ignore_index=True)
        instructors.to_csv(FILES['instructors'], index=False, encoding='utf-8-sig')
        print(f"The record has been added :)")
    except Exception as e:
        print(f"An error occurred while adding the record{e}")

def add_enrollment(enrollment_data):
    try:
        _validate_not_null(enrollment_data, ['StudentID','CourseID','Semester', 'Year'])
        _validate_grade(enrollment_data['Grade'])
        enrollments = pd.read_csv(FILES['enrollments'])
        enrollments = pd.concat([enrollments, pd.DataFrame([enrollment_data])], ignore_index=True)
        enrollments.to_csv(FILES['enrollments'], index=False, encoding='utf-8-sig')
        print(f"The record has been added :)")
    except Exception as e:
        print(f"An error occurred while adding the record{e}")

# ------ Update Records ------
def update_student(id, updated_data):
    try:
        _validate_not_null(updated_data, ['StudentID', 'FirstName', 'LastName', 'DateOfBirth', 'Major'])
        _validate_dob(updated_data['DateOfBirth'])
        if not os.path.exists(FILES['students']):
            raise FileNotFoundError("No found file :(")
        
        updated = pd.read_csv(FILES['students'], dtype = {'Phone' : str})
        mask = updated['StudentID'] == id
        
        if updated[mask].empty:
            print("No matching data found :(")
            return
        
        if 'StudentID' in updated_data:
            new_id = updated_data['StudentID']
            
            # Verify that the ID is not duplicate
            if (new_id != id) and (new_id in updated['StudentID'].values):
                raise ValueError("The entered recording ID already exists!")
            
            # Update ID in associated record
            _update_related_ids(FILES['enrollments'], 'StudentID', id, new_id)
        
        # Update date 
        for key, value in updated_data.items():
            if key == 'Phone':
                value == str(value)
            updated.loc[mask,key] = value
        
        updated.to_csv(FILES['students'], index=False, encoding='utf-8-sig')
        print("Data updated :)")
        
    except Exception as e:
        print(f"An error occurred : {e}")

def update_course(id, updated_data):
    try:
        _validate_not_null(updated_data, ['CourseID','CourseName','Credits', 'Department'])
        _validate_credits(updated_data['Credits'])
        if not os.path.exists(FILES['courses']):
            raise FileNotFoundError("No found file :(")
        
        updated = pd.read_csv(FILES['courses'])
        mask = updated['CourseID'] == id

        if updated[mask].empty:
            print("No matching data found :(")
            return
        
        if 'CourseID' in updated_data:
            new_id = updated_data['CourseID']
            
            # Verify that the ID is not duplicate
            if (new_id != id) and (new_id in updated['CourseID'].values):
                raise ValueError("The entered recording ID already exists!")
            
            # Update ID in associated record
            _update_related_ids(FILES['enrollments'], 'CourseID', id, new_id)
        
        # Update date 
        for key, value in updated_data.items():
            updated.loc[mask,key] = value           
        
        updated.to_csv(FILES['courses'], index=False, encoding='utf-8-sig')
        print("Data updated :)")
        
    except Exception as e:
        print(f"An error occurred : {e}")


def update_instructor(id, updated_data):
    try:
        _validate_not_null(updated_data, ['InstructorID','FirstName','LastName', 'Department'])
        _validate_unique('Email', updated_data['Email'], FILES['instructors'])
        if not os.path.exists(FILES['instructors']):
            raise FileNotFoundError("No found file :(")
        
        updated = pd.read_csv(FILES['instructors'])
        mask = updated['InstructorID'] == id

        if updated[mask].empty:
            print("No matching data found :(")
            return
        
        if 'InstructorID' in updated_data:
            new_id = updated_data['InstructorID']
            
            # Verify that the ID is not duplicate
            if (new_id != id) and (new_id in updated['InstructorID'].values):
                raise ValueError("The entered recording ID already exists!")
            
        # Update date 
        for key, value in updated_data.items():
            updated.loc[mask,key] = value           
        
        updated.to_csv(FILES['instructors'], index=False, encoding='utf-8-sig')
        print("Data updated :)")
        
    except Exception as e:
        print(f"An error occurred : {e}")

def update_enrollment(student_id, course_id, semester, year, updated_data):
    try:
        student_id = str(student_id)
        course_id = str(course_id)
        year = str(year)
        
        _validate_not_null(updated_data, ['StudentID','CourseID','Semester', 'Year'])
        if 'Grade' in updated_data:
            _validate_grade(updated_data['Grade'])
        
        if not os.path.exists(FILES['enrollments']):
            raise FileNotFoundError("No found file :(")
        
        enrollments = pd.read_csv(FILES['enrollments'], dtype={
            'StudentID': str,
            'CourseID': str,
            'Year': str
        })
        
        mask = (
            (enrollments['StudentID'] == student_id) &
            (enrollments['CourseID'] == course_id) &
            (enrollments['Semester'] == semester) &
            (enrollments['Year'] == year)
        )
                
        if enrollments[mask].empty:
            print("No matching data found :(")
            return
        
        for key, value in updated_data.items():
            enrollments.loc[mask, key] = value
        
        enrollments.to_csv(FILES['enrollments'], index=False, encoding='utf-8-sig')
        print("Data updated :)")
        
    except Exception as e:
        print(f"An error occurred : {e}")

# ------ Delete Records ------
def delete_student(student_id):
    _delete_related_records(FILES['students'], FILES['enrollments'], 'StudentID', student_id)
    if os.path.exists(FILES['students']):
        df = pd.read_csv(FILES['students'])
        data = df[df['StudentID'] == student_id]
        df = df[df['StudentID'] != student_id]
        df.to_csv(FILES['students'], index=False, encoding='utf-8-sig')
        if not data.empty:
            print("The record has been deleted :)")
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def delete_course(course_id):
    _delete_related_records(FILES['courses'], FILES['enrollments'], 'CourseID', course_id)
    if os.path.exists(FILES['courses']):
        df = pd.read_csv(FILES['courses'])
        data = df[df['CourseID'] == course_id]
        df = df[df['CourseID'] != course_id]
        df.to_csv(FILES['courses'], index=False, encoding='utf-8-sig')
        if not data.empty:
            print("The record has been deleted :)")
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def delete_instructor(instructor_id):
    if os.path.exists(FILES['instructors']):
        df = pd.read_csv(FILES['instructors'])
        data = df[df['InstructorID'] == instructor_id]
        df = df[df['InstructorID'] != instructor_id]
        df.to_csv(FILES['instructors'], index=False, encoding='utf-8-sig')
        if not data.empty:
            print("The record has been deleted :)")
        else:
            print(f"No Data Found :(")
    else:
        print("Error : The file does not exist!")

def delete_enrollment(student_id, course_id, sem, year):
    try:
        if not os.path.exists(FILES['enrollments']):
            print("Error : The file does not exist!")
            return

        enrollments = pd.read_csv(FILES['enrollments'])

        student_id = str(student_id)
        course_id = str(course_id)
        year = str(year)
        
        mask = (
            (enrollments['StudentID'].astype(str) == student_id) & 
            (enrollments['CourseID'].astype(str) == course_id) & 
            (enrollments['Semester'] == sem) & 
            (enrollments['Year'].astype(str) == year)
        )
        
        if enrollments[mask].empty:
            print("No Data Found :(")
            return
        
        enrollments = enrollments[~mask]
        enrollments.to_csv(FILES['enrollments'], index=False, encoding='utf-8-sig')
        print("The record has been deleted :)")
        
    except Exception as e:
        print(f"An error occurred: {e}")

# ------ Main Implementation ------

def main():
    # Implement the addition
    add_student({
        'StudentID': 33,
        'FirstName': 'محمد',
        'LastName': 'علي',
        'DateOfBirth': '2003-05-15',
        'Major': 'كلية الهندسة',
        'Address': 'طرابلس',
        'Phone': '0912345678'
    })

    add_course({
        'CourseID': 'C41',
        'CourseName': 'رياضيات هندسية',
        'Credits': 3,
        'Department': 'كلية الهندسة'
    })
    add_instructor({
        'InstructorID': 'I4',
        'FirstName': 'أحمد',
        'LastName': 'محمود',
        'Department': 'كلية الهندسة',
        'Rank': 'أستاذ',
        'Email': 'ahmed@univ.5du'
    })

    add_enrollment({
        'StudentID': 'S4',
        'CourseID': 'C4',
        'Semester': 'الفصل الأول',
        'Year': 2023,
        'Grade': 85
    }) 

    # Implement the deletion
    delete_student(20250007)
    delete_course('C0007')
    delete_instructor('I0007')
    delete_enrollment(20250070,'C0181','الفصل الأول',2023)

    # Implement the update
    update_student(20259432, {
        'StudentID': 12345698,
        'FirstName': 'محمد',
        'LastName': 'علي',
        'DateOfBirth': '2005-05-15',
        'Major': 'كلية الهندسة',
        'Address': 'طرابلس',
        'Phone': '0912345678'
    })

    update_course('C4996', {
        'CourseID': 'C10',
        'CourseName': 'رياضيات هندسية',
        'Credits': 3,
        'Department': 'كلية الهندسة'
    })

    update_instructor('I0006', {
        'InstructorID': 'I20',
        'FirstName': 'أحمد',
        'LastName': 'محمود',
        'Department': 'كلية الهندسة',
        'Rank': 'أستاذ',
        'Email': 'ahmed@univ.520du'
    })

    update_enrollment(20258170,'C9564','الفصل الثاني',2021,{
        'StudentID': 25,
        'CourseID': 'CCC',
        'Semester': 'الفصل الأول',
        'Year': 2023,
        'Grade': 85
        })

if __name__ == "__main__":
    main()