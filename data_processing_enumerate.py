students = ["Alice", "Bob", "Carol", "David", "Eve"]
scores = [85, 92, 78, 88, 95]


# Create a Numbered List of Students
def enumerate_students(students):
    """Return a numbered list of students."""
    return [f"{index + 1}: {student}" for index, student in enumerate(students)]

print(enumerate_students(students))

# Pair Students with Their Scores Using enumerate()
def pair_students_with_scores(students, scores):
    """Return a list of tuples pairing students with their scores."""
    return [(student, scores[index]) for index, student in enumerate(students)]

print(pair_students_with_scores(students, scores))

# Identify and print the positions (indices) of students who scored above 90
def high_scorers_indices(students, scores, threshold=90):
    """Return indices of students who scored above a given threshold."""
    return [index for index, score in enumerate(scores) if score > threshold]

print(high_scorers_indices(students, scores))

# Create a dictionary where keys are positions (starting from 0) and values are the student names.
def students_dict(students):
    """Return a dictionary with student names indexed by their positions."""
    return {index: student for index, student in enumerate(students)}

print(students_dict(students))
