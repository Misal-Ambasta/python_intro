students = [
    (101, "Alice", 85, 20),
    (102, "Bob", 92, 19),
    (103, "Carol", 78, 21),
    (104, "David", 88, 20)
]

# Identify and print the student who has the highest grade from the list.
def highest_grade_student(students):
    """Return the student with the highest grade."""
    students=sorted(students,key=lambda x:x[2],reverse=True)
    print(students)
    return students[0][1]

# Generate a new list containing only the name and grade of each student in the format: ("Alice", 85)
def student_names_and_grades(students):
    li = []
    for i in students:
        li.append((i[1], i[2]))

    return li   
    

#students[0][2] = 90

