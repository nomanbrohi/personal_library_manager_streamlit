import json

def add_book(library):
    print('\nPlease Enter your Books Details')
    input_title = input('Enter Book Title: ')
    input_author = input('Enter Book Author: ')
    input_publication = input('Enter Book Publication: ')
    input_genre = input('Genre: ')
    input_read = input('Have you read this book? (yes/no): ').lower() == 'yes'

    new_book = {
        "title": input_title,
        "author": input_author,
        "publication": input_publication,
        "genre": input_genre,
        "read": input_read
    }
    library.append(new_book)
    print("Book added successfully!")

def remove_book(library):
    title = input("Enter Title to remove book: ")
    found = False
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            print("Book removed successfully")
            found = True
            break
    if not found:
        print("Book not found")

def search_book(library):
    search_term = input("Please Enter Book Title or Author name: ")
    found_books = []
    for book in library:
        if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower():
            found_books.append(book)
    if found_books:
        print("Matching Books:")
        for book in found_books:
            print(book)
    else:
        print("No books found.")

def all_books(library):
    if not library:
        print("Your library is empty!")
    else:
        print("Your Library:")
        for i, book in enumerate(library, 1):
            print(f"{i}. Title: {book['title']}, Author: {book['author']}, Publication: {book['publication']}, Genre: {book['genre']}, Read: {'Yes' if book['read'] else 'No'}")

def stats(library):
    total_books = len(library)
    read_books = sum(book.get("read", False) for book in library)
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    print(f"Total Books: {total_books}")
    print(f"Books Read: {read_books} ({percentage_read:.1f}%)")

def save_library(library, filename="library.json"):
    with open(filename, "w") as file:
        json.dump(library, file)
    print("Library saved to file.")

def load_library(filename="library.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No saved library found. Starting with an empty library.")
        return []

def menu():
    library = load_library()
    while True:
        print("\nWelcome to Personal Library Manager!")
        menu_options = ['Add a book', 'Remove a book', 'Search for a book', 'Display all books', 'Display statistics', 'Exit']
        for i, option in enumerate(menu_options, 1):
            print(f"{i} - {option}")
        user_input = input("Enter menu index (or 'q' to quit): ")
        if user_input.lower() == 'q':
            save_library(library)
            print("Goodbye!")
            break
        try:
            user_input = int(user_input)
            if user_input == 1:
                add_book(library)
            elif user_input == 2:
                remove_book(library)
            elif user_input == 3:
                search_book(library)
            elif user_input == 4:
                all_books(library)
            elif user_input == 5:
                stats(library)
            elif user_input == 6:
                save_library(library)
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")
        except ValueError:
            print("Please enter a valid number.")

menu()