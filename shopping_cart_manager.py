shopping_cart= []

def add_item(item):
    shopping_cart.append(item)

def remove_item(item):
    if item in shopping_cart:
        shopping_cart.remove(item)

def remove_last_item():
    if shopping_cart:
        shopping_cart.pop()

def display_alphabetically():
    for item in sorted(shopping_cart):
        print(item)

def display_cart_contents_indices():
    for index, item in enumerate(shopping_cart):
        print(f"{index}: {item}")