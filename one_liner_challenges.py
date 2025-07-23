# 5 different one-liner solutions list comprehensions, lambda functions, and built-in functions like map(), filter(), and reduce()

def one_liner_challenges():
    # 1. List comprehension to create a list of squares from 1 to 10
    squares = [x**2 for x in range(1, 11)]
    
    # 2. Lambda function to double each number in a list
    numbers = [1, 2, 3, 4, 5]
    doubled = list(map(lambda x: x * 2, numbers))
    
    # 3. Filter even numbers from a list
    even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
    
    # 4. Reduce to find the sum of a list
    from functools import reduce
    total_sum = reduce(lambda x, y: x + y, numbers)
    
    # 5. Create a dictionary with numbers and their cubes
    cubes_dict = {x: x**3 for x in range(1, 6)}
    
    return squares, doubled, even_numbers, total_sum, cubes_dict

print(one_liner_challenges())