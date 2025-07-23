grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]

def slice_grades(grades, start, end):
    """Return a slice of the grades list from start to end indices."""
    return grades[start:end]

print(slice_grades(grades, 2, 8))

# Use list comprehension to find grades above 85
print([i for i in grades if i > 85])

# Replace the grade at index 3 with 95
grades[3] = 95

# Append three new grades
grades.extend([82, 88, 91])

# Sort in descending order and display the top 5 grades
grades.sort(reverse=True)
print(grades[:5])