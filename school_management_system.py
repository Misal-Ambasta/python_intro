school = {
    "Math": {
        "teacher": "Mr. Smith",
        "students": [("Alice", 85), ("Bob", 92), ("Carol", 78)]
    },
    "Science": {
        "teacher": "Ms. Johnson",
        "students": [("David", 88), ("Eve", 94), ("Frank", 82)]
    }
}

# Iterate through all classes and print the name of each teacher.
def print_teachers(school):
    for subject, details in school.items():
        print(f"Teacher for {subject}: {details['teacher']}")

print_teachers(school)

# For each class, calculate and display the average grade of the students.
def average_grades(school):
    for subject, details in school.items():
        students = details['students']
        if students:
            avg_grade = sum(grade for _, grade in students) / len(students)
            print(f"Average grade for {subject}: {avg_grade:.2f}")

average_grades(school)

# Identify the student with the highest grade among all students across every class.

def highest_student_grade(school):  
    highest_student = None
    highest_grade = -1
    for details in school.values():
        for student, grade in details['students']:
            if grade > highest_grade:
                highest_grade = grade
                highest_student = student
    print(f"Highest student: {highest_student} with grade {highest_grade}")


highest_student_grade(school)

# Use tuple unpacking to extract and work with student names and grades separately.

def student_names_and_grades(school):
    for subject, details in school.items():
        for student, grade in details['students']:
            print(f"Student: {student}, Grade: {grade}")