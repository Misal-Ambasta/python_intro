# Age validator using try-except block, it will check age between 1 and 120, will also throw error for string input
def validate_age_input(age_input):
    try:
        age = int(age_input)
        if age < 1 or age > 120:
             print("Age must be between 1 and 120.")
             return False
        return age
    except ValueError as e:
         print(f"Invalid input for age. Please enter a valid integer between 1 and 120.")
         return False


age = input("Enter your age: ")
valid_age = validate_age_input(age)
if valid_age:
    print(f"You entered a valid age: {valid_age}")
