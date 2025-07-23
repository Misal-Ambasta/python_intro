employees = [
    ("Alice", 50000, "Engineering"),
    ("VBob", 60000, "Marketing"),
    ("Carol", 55000, "Engineering"),
    ("David", 45000, "Sales")
]


# Sort the list of employees by salary in both ascending and descending order.

def sort_by_salary(emp):
    sort_by_ascending = sorted(emp, key=lambda x: x[1])
    print(sort_by_ascending)
    sort_by_descending = sorted(emp, key=lambda x:x[1], reverse=True)
    print(sort_by_descending)

sort_by_salary(employees)

# First sort by department name alphabetically, then by salary within each department.

def sort_by_dept_salary(emp):
    emp_sort = sorted(emp, key=lambda x: (x[2], x[1]))
    print(emp_sort)

sort_by_dept_salary(employees)

# Reverse the order of the original list of employees without modifying the original.

def reverse_order(emp):
    new_emp = emp[::-1]
    print(new_emp)

reverse_order(employees)

# Sort employees based on the length of their names.

def sort_length_names(emp):
    new_emp = sorted(emp, key=lambda x:len(x[0]))
    print(new_emp)

# Use .sort() when modifying the original list and sorted() when creating a new sorted list. Demonstrate both methods.

def sort_vs_sorted(emp):
    emp.sort()
    print(emp)

sort_vs_sorted(employees)