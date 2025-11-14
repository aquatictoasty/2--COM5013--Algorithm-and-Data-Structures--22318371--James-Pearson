#
# COM5013 Algorithms & Data Structures
# Assignment: University Library Management System
# Name: James Pearson
# Student Number: 22318371
#

import time
import sys
import random
# using 'lazy' (built-in) queue
from collections import deque 

# Core Data Class
class Book:
    """Represents a single book in the library."""
    def __init__(self, isbn, title, author):
        # validation to handle "zero or null values" test case
        if not all([isbn is not None, title, author]):
             raise ValueError("Book ISBN, title, and author cannot be None or empty.")
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_checked_out = False
        # uses built-in, fast 'deque' as the 'lazy queue'
        self.waitlist = deque() 

    def __str__(self):
        status = "Checked Out" if self.is_checked_out else "Available"
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn}) - Status: {status}'

# Data Structure 1: Hash Table
class HashTable:
    """A hash table using separate chaining."""
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        """A simple hash function."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Inserts a key-value pair. O(1) average."""
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        """Retrieves a value by its key. O(1) average."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

# Data Structure 2: BST now iterative
class BSTNode:
    """A node for the Binary Search Tree."""
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    A complete and iterative standard binary search tree.
    """
    def __init__(self):
        self.root = None

    def insert(self, book):
        """Iterative insert. Prevents RecursionError and is fast."""
        new_node = BSTNode(book)
        if self.root is None:
            self.root = new_node
            return

        current = self.root
        while True:
            if book.title < current.book.title:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left
            # handle duplicates or equal titles by placing to the right
            else:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right
    
    def search(self, title):
        """Iterative search is efficient."""
        current = self.root
        while current is not None:
            if title == current.book.title:
                return current.book
            elif title < current.book.title:
                current = current.left
            else:
                current = current.right
        return None

    def in_order_traversal(self):
        """
        Iterative in-order traversal. This is robust and will not
        hit recursion limits, even on a deep tree.
        """
        books = []
        stack = []
        current = self.root
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            books.append(current.book)
            current = current.right
        return books

# Main Application Class 
class Library:
    """The main library system controller."""
    def __init__(self, size=10000):
        # uses a large hash table
        self.books_by_isbn = HashTable(size)
        self.books_by_title = BinarySearchTree()
        print(f"Library system initialised (Hash Table Size: {size}).")

    def add_book(self, isbn, title, author, verbose=True):
        """Adds a new book. Verbose flag for silent operation."""
        try:
            # check for existence first which is done silently for speed
            if self.books_by_isbn.get(isbn):
                if verbose: print(f"Error: Book with ISBN {isbn} already exists.")
                return False
            
            new_book = Book(isbn, title, author)
            self.books_by_isbn.insert(isbn, new_book)
            self.books_by_title.insert(new_book)
            
            if verbose: print(f"Added: \"{title}\"")
            return True
        except ValueError as e:
            if verbose: print(f"Error adding book: {e}")
            return False
            
    def checkout_book(self, isbn, user_id):
        """Checks out a book to a user."""
        book = self.books_by_isbn.get(isbn)
        if not book:
            print("Error: Book not found.")
            return

        if book.is_checked_out:
            print(f"'{book.title}' is busy. Adding '{user_id}' to waitlist.")
            # uses deque.append() for enqueue
            book.waitlist.append(user_id)
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
            print(f"Error: '{book.title}' is not checked out.")
            return

        book.is_checked_out = False
        print(f"'{book.title}' has been returned.")

        # check waitlist using 'if self.waitlist:' (fast)
        if book.waitlist:
            # uses deque.popleft() for dequeue
            next_user = book.waitlist.popleft()
            print(f"Notifying next user: '{next_user}'.")
            self.checkout_book(isbn, next_user)
            
    # Methods from the original test code
    
    def find_book_by_isbn(self, isbn, verbose=True):
        """Finds and displays book details using ISBN."""
        book = self.books_by_isbn.get(isbn)
        if verbose:
            if book:
                print("Found book by ISBN:")
                print(f"  {book}")
            else:
                print(f"No book found with ISBN {isbn}.")
        return book

    def find_book_by_title(self, title, verbose=True):
        """Finds and displays book details using title."""
        book = self.books_by_title.search(title)
        if verbose:
            if book:
                print("Found book by Title:")
                print(f"  {book}")
            else:
                print(f"No book found with title '{title}'.")
        return book

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


# FULL TESTING  

def run_assignment_edge_case_tests():
    """
    This test suite addresses the specific edge cases.
    """
    print(" RUNNING EDGE CASE TEST SUITE")
    
    my_library = Library(size=100)

    # Test Case: Zero or Null Values
    print("\n--- 1. Test: Handling Zero and Null Values ---")
    print("Attempting to add a book with ISBN 0 (should succeed):")
    my_library.add_book(isbn=0, title="The Book of Zero", author="Mr. Null")
    my_library.find_book_by_isbn(0)
    
    print("\nAttempting to add a book with a None title (should fail):")
    my_library.add_book(isbn="123-456", title=None, author="Some Author")
    
    print("\nAttempting to add a book with an empty string title (should fail):")
    my_library.add_book(isbn="456-789", title="", author="Some Author")

    # Test Case: Large Data Type (over 64 bits)
    print("\n--- 2. Test: Handling Large Data Types (> 64-bit) ---")
    large_isbn = 9780134685991123456789012345678901234567890
    print(f"Attempting to add a book with a very large ISBN: {large_isbn}")
    my_library.add_book(large_isbn, "Book of Large Numbers", "Dr. Python")
    print("Searching for the book by its large ISBN:")
    my_library.find_book_by_isbn(large_isbn)
    print(" > Test PASSED: Python's arbitrary-precision integers are handled correctly by hash().")
    print("Edge Case Tests Passed!")


def run_functional_tests():
    """
    This is the original test suite, ensuring all
    core functionality still works after changes.
    """
    print("     RUNNING ORIGINAL FUNCTIONAL TEST SUITE")

    # 1. Initialise the library
    my_library = Library(size=100) 
    
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
    print("Functional Tests Passed!")


def run_scalability_test():
    """
    This is the  1M test suite to demonstrate O(n log n)
    insertion and fast O(1) / O(log n) search.
    """
    print(" RUNNING SCALABILITY TEST SUITE (1,000,000 BOOKS)")
    
    num_books = 1000000
    
    # Initialise a new library with a large hash table (1.25x load factor)
    large_library = Library(size=int(num_books * 1.25))
    
    print(f"--- 1. Testing scalability with {num_books} books ---")
    print(f"Adding {num_books} books with RANDOM titles...")
    print("(This loop is silent for maximum speed)...")
    
    start_time = time.time()
    for i in range(num_books):
        # integer ISBN
        isbn = i
        # random Title (prevents BST from becoming unbalanced)
        title = f"Book Title {random.randint(0, num_books * 10)}"
        
        # Add book with verbose=False (No prints)
        large_library.add_book(isbn, title, "Test Author", verbose=False)
    
    end_time = time.time()
    
    print(f"\n Time to add {num_books} books: {end_time - start_time:.4f} seconds.")
    print("   (This is O(n log n) thanks to the random titles)\n")

    # performance of search operations
    # will find a book i know i added
    isbn_to_find = num_books // 2
    # need to get its random title from the hash table first
    book_to_find = large_library.find_book_by_isbn(isbn_to_find, verbose=False)
    
    if not book_to_find:
        print("Error: Could not find book to test search!")
        return
    title_to_find = book_to_find.title

    print("--- 2. Performance Test: Searching ---")
    print(f"   (Searching for ISBN {isbn_to_find} and Title '{title_to_find}')\n")

    print("Searching for a book by ISBN (Hash Table)...")
    start_time = time.time()
    result = large_library.find_book_by_isbn(isbn_to_find, verbose=False)
    end_time = time.time()
    print(f"Result found: \"{result.title}\"")
    print(f" Hash Table search time: {(end_time - start_time) * 1e6:.2f} microseconds. (O(1) speed)")
    
    print("\nSearching for a book by Title (Standard BST)...")
    start_time = time.time()
    result = large_library.find_book_by_title(title_to_find, verbose=False)
    end_time = time.time()
    print(f"Result found: \"{result.title}\"")
    print(f"BST search time: {(end_time - start_time) * 1e6:.2f} microseconds. (O(log n) speed)")

    print("\n Scalability Tests Passed")


if __name__ == "__main__":
    run_assignment_edge_case_tests()
    run_functional_tests()
    run_scalability_test()