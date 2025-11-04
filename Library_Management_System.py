#
# COM5013 Algorithms & Data Structures
# Assignment: University Library Management System
# Name: James Pearson
# Student Number: 22318371
#

# Core Data Class
class Book:
    """Represents a single book in the library."""
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_checked_out = False
        self.waitlist = Queue()  # Each book has its own waiting list queue

    def __str__(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn}) - Status: {status}'

# Data Structure Implementations

# 1. Queue (for Book Waitlists) - Implemented with a Linked List
class Node:
    """A node for use in the linked list queue."""
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    """A First-In, First-Out (FIFO) queue implemented using a linked list."""
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def enqueue(self, item):
        """Adds an item to the end of the queue. O(1)"""
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        """Removes and returns the item from the front of the queue. O(1)"""
        if self.is_empty():
            return None
        item = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        self._size -= 1
        return item
    
    def peek(self):
        """Returns the front item without removing it."""
        return self.front.data if not self.is_empty() else None

    def size(self):
        return self._size

# 2. Hash Table (for Primary Storage by ISBN) - Implemented with Separate Chaining
class HashTable:
    """A hash table using separate chaining for collision resolution."""
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        """A simple hash function to map a key to an index."""
        # A simple modulo hash for string ISBNs
        return hash(key) % self.size

    def insert(self, key, value):
        """Inserts a key-value pair into the hash table. O(1) average."""
        index = self._hash(key)
        bucket = self.table[index]
        # Check if key already exists, if so, update it
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        # Otherwise, append the new key-value pair
        bucket.append((key, value))

    def get(self, key):
        """Retrieves a value by its key. O(1) average."""
        index = self._hash(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        return None # Key not found

    def delete(self, key):
        """Deletes a key-value pair. O(1) average."""
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return

# 3. Binary Search Tree (for Secondary Search by Title)
class BSTNode:
    """A node for use in the Binary Search Tree."""
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

class BinarySearchTree:
    """A binary search tree to store and search books by title."""
    def __init__(self):
        self.root = None

    def insert(self, book):
        """Inserts a book into the BST, ordered by title. O(log n) average."""
        if self.root is None:
            self.root = BSTNode(book)
        else:
            self._insert_recursive(self.root, book)

    def _insert_recursive(self, current_node, book):
        if book.title < current_node.book.title:
            if current_node.left is None:
                current_node.left = BSTNode(book)
            else:
                self._insert_recursive(current_node.left, book)
        else:
            if current_node.right is None:
                current_node.right = BSTNode(book)
            else:
                self._insert_recursive(current_node.right, book)

    def search(self, title):
        """Searches for a book by title. O(log n) average."""
        return self._search_recursive(self.root, title)

    def _search_recursive(self, current_node, title):
        if current_node is None or current_node.book.title == title:
            return current_node.book if current_node else None
        
        if title < current_node.book.title:
            return self._search_recursive(current_node.left, title)
        else:
            return self._search_recursive(current_node.right, title)

    def in_order_traversal(self):
        """Performs an in-order traversal to get all books sorted by title."""
        books = []
        self._in_order_recursive(self.root, books)
        return books

    def _in_order_recursive(self, current_node, books):
        if current_node:
            self._in_order_recursive(current_node.left, books)
            books.append(current_node.book)
            self._in_order_recursive(current_node.right, books)


# Main Application Class
class Library:
    """The main library system controller."""
    def __init__(self):
        # The two primary data structures for storing book data
        self.books_by_isbn = HashTable()
        self.books_by_title = BinarySearchTree()
        print("Library system initialized.")

    def add_book(self, isbn, title, author):
        """Adds a new book to the library."""
        if self.books_by_isbn.get(isbn):
            print(f"Error: Book with ISBN {isbn} already exists.")
            return
        
        new_book = Book(isbn, title, author)
        self.books_by_isbn.insert(isbn, new_book)
        self.books_by_title.insert(new_book)
        print(f"Added: {new_book.title}")

    def checkout_book(self, isbn, user_id):
        """Checks out a book to a user."""
        book = self.books_by_isbn.get(isbn)
        if not book:
            print("Error: Book not found.")
            return

        if book.is_checked_out:
            print(f"'{book.title}' is currently checked out. Adding user '{user_id}' to waitlist.")
            book.waitlist.enqueue(user_id)
        else:
            book.is_checked_out = True
            print(f"'{book.title}' checked out to user '{user_id}'.")

    def return_book(self, isbn):
        """Returns a book to the library."""
        book = self.books_by_isbn.get(isbn)
        if not book:
            print("Error: Book not found.")
            return

        if not book.is_checked_out:
            print(f"Error: '{book.title}' is not currently checked out.")
            return

        book.is_checked_out = False
        print(f"'{book.title}' has been returned.")

        if not book.waitlist.is_empty():
            next_user = book.waitlist.dequeue()
            print(f"Notifying next user on waitlist: '{next_user}'.")
            # In a hyperthetical real system, this would trigger an email or notification
            self.checkout_book(isbn, next_user)

    def find_book_by_isbn(self, isbn):
        """Finds and displays book details using ISBN."""
        book = self.books_by_isbn.get(isbn)
        if book:
            print("Found book by ISBN:")
            print(f"  {book}")
        else:
            print(f"No book found with ISBN {isbn}.")

    def find_book_by_title(self, title):
        """Finds and displays book details using title."""
        book = self.books_by_title.search(title)
        if book:
            print("Found book by Title:")
            print(f"  {book}")
        else:
            print(f"No book found with title '{title}'.")

    def list_all_books(self):
        """Lists all books in the library, sorted alphabetically by title."""
        print("\n--- Library Catalogue (Alphabetical by Title) ---")
        sorted_books = self.books_by_title.in_order_traversal()
        if not sorted_books:
            print("The library has no books.")
            return
        for book in sorted_books:
            print(book)
        print("-------------------------------------------------")

# Testing and Demonstration 
if __name__ == "__main__":
    
    # 1. Initialise the library
    my_library = Library()
    
    # 2. Test handling of an empty data structure
    print("\n--- Test: Operations on Empty Library ---")
    my_library.list_all_books()
    my_library.find_book_by_isbn("000-0-00-000000-0")
    
    # 3. Add books to the library
    print("\n--- Test: Adding Books ---")
    my_library.add_book("978-0-262-03384-8", "Introduction to Algorithms", "Thomas H. Cormen")
    my_library.add_book("978-0-321-76572-3", "The C++ Programming Language", "Bjarne Stroustrup")
    my_library.add_book("978-0-13-235088-4", "Clean Code", "Robert C. Martin")
    my_library.add_book("978-1-491-90424-4", "You Don't Know JS: Up & Going", "Kyle Simpson")
    my_library.add_book("978-0-13-468599-1", "Effective Java", "Joshua Bloch")

    # Display the full catalogue
    my_library.list_all_books()
    
    # 4. Test feature: Searching for books
    print("\n--- Test: Searching ---")
    my_library.find_book_by_isbn("978-0-13-235088-4") 
    my_library.find_book_by_isbn("000-0-00-000000-0") # Non-existent
    
    my_library.find_book_by_title("Clean Code")
    my_library.find_book_by_title("Non-Existent Book") # Non-existent
    
    # 5. Test feature: Checking out a book
    print("\n--- Test: Checkout Process ---")
    my_library.checkout_book("978-0-13-235088-4", "user_alice")
    my_library.find_book_by_isbn("978-0-13-235088-4") # Check status has changed
    
    # 6. Test feature: Waitlisting
    print("\n--- Test: Waitlist ---")
    my_library.checkout_book("978-0-13-235088-4", "user_bob") 
    my_library.checkout_book("978-0-13-235088-4", "user_charlie")
    
    # 7. Test feature: Returning a book and processing the waitlist
    print("\n--- Test: Returning a Book ---")
    my_library.return_book("978-0-13-235088-4")
    
    my_library.find_book_by_isbn("978-0-13-235088-4")
    
    print("\n--- Test: Returning Again ---")
    my_library.return_book("978-0-13-235088-4")
    my_library.find_book_by_isbn("978-0-13-235088-4")

    # 8. Final state of the library
    my_library.list_all_books()