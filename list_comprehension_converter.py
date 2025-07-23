# List Comprehension Converter

square = [i * i for i in range(10)]

print(square)

# square for odd numbers
square_odd = [i * i for i in range(20) if i % 2 != 0]

print(square_odd)

pairs = [(x, y) for x in range(3) for y in range(3)]
print(pairs)

