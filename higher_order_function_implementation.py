def custom_map(func, iterable):
    """Applies a function to every item of an iterable and returns a list of results."""
    return [func(item) for item in iterable]

def custom_filter(func, iterable):
    """Filters items in an iterable based on a function and returns a list of results."""
    return [item for item in iterable if func(item)]

def custom_reduce(func, iterable, initial=None):
    """Reduces an iterable to a single value using a binary function."""
    from functools import reduce
    return reduce(func, iterable, initial) if initial is not None else reduce(func, iterable)


print(custom_map(lambda x: x * 2, [1, 2, 3, 4]))
print(custom_filter(lambda x: x > 2, [1, 2, 3, 4]))
print(custom_reduce(lambda x, y: x + y, [1, 2, 3, 4], 0))
