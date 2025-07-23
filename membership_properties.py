fruits_list = ["apple", "banana", "orange", "apple", "grape"]
fruits_tuple = ("apple", "banana", "orange")
fruits_set = {"apple", "banana", "orange", "grape"}
fruits_dict = {"apple": 5, "banana": 3, "orange": 8, "grape": 2}

# Test whether "apple" is present in each data structure.
def check_membership(item, collection):
    if isinstance(collection, list):
        return item in collection
    elif isinstance(collection, tuple):
        return item in collection
    elif isinstance(collection, set):
        return item in collection
    elif isinstance(collection, dict):
        return item in collection.keys()
    else:
        return False

print(check_membership("apple", fruits_list))  # True
print(check_membership("apple", fruits_tuple))  # True
print(check_membership("apple", fruits_set))    # True  

# Display the number of elements in each structure using len()
def display_length(collection):
    return len(collection)

print(display_length(fruits_list))  # 5
print(display_length(fruits_tuple))  # 3
print(display_length(fruits_set))    # 4
print(display_length(fruits_dict))   # 4

# Loop through each structure and print its contents.
def print_contents(collection):
    if isinstance(collection, list) or isinstance(collection, tuple):
        for item in collection:
            print(item)
    elif isinstance(collection, set):
        for item in collection:
            print(item)
    elif isinstance(collection, dict):
        for key, value in collection.items():
            print(f"{key}: {value}")