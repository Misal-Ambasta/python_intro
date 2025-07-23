
book_dict = { "Atomic Habits": "James Clear" }

def add_book(book_name, author_name):
    book_dict[book_name] = author_name

def search_book(book_name):
    return book_dict.get(book_name, "Book not found")

def display_inventory():
    if not book_dict:
        return "No books in inventory."
    return "\n".join([f"- Book: {book} | {author}" for book, author in book_dict.items()])

add_book("1984", "George Orwell")
add_book("To Kill a Mockingbird", "Harper Lee")

print("Inventory:")
print(display_inventory())