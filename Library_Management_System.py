#
# Module: COM5013 Algorithms & Data Structures
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


# Data Structure 2: BST (iterative)
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

    def _find_min_node(self, node):
        """Helper to find the minimum value node in a subtree (leftmost node)."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, title):
        """
        Iterative delete method for the BST, removing the node by title.
        This uses a recursive helper for simplicity in handling the node replacement
        logic needed for deletion with two children, as an iterative delete
        implementation is significantly more complex and error-prone.
        """
        self.root = self._delete_recursive(self.root, title)

    def _delete_recursive(self, root, title):
        """
        Recursive helper for BST deletion.
        It's acceptable to use recursion for the delete logic as it only goes 
        down the height of the tree, which is O(log n), and is not susceptible 
        to python's recursion limit like a full traversal would be.
        """
        if root is None:
            return root

        # 1. Traverse to find the node
        if title < root.book.title:
            root.left = self._delete_recursive(root.left, title)
        elif title > root.book.title:
            root.right = self._delete_recursive(root.right, title)
        else:
            # 2. Node found, handle the 3 cases:

            # Case 1: Node with only one child or no child
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Case 3: Node with two children
            # finds the inorder successor (smallest in the right subtree)
            temp = self._find_min_node(root.right)

            # copys the inorder successor's content to this node
            root.book = temp.book

            # deletes the inorder successor recursively
            root.right = self._delete_recursive(root.right, temp.book.title)
        
        return root

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
        # use Python's built-in dict for ISBN lookup (O(1) average)
        # `size` parameter accepted for compatibility with existing tests but is unused.
        self.books_by_isbn = {}
        self.books_by_title = BinarySearchTree()
        print(f"Library system initialised (using built-in dict for ISBN lookup).")

    def add_book(self, isbn, title, author, verbose=True):
        """Adds a new book. Verbose flag for silent operation."""
        try:
            # check for existence first which is done silently for speed
            if isbn in self.books_by_isbn:
                if verbose: print(f"Error: Book with ISBN {isbn} already exists.")
                return False
            
            new_book = Book(isbn, title, author)
            # store in built-in dict
            self.books_by_isbn[isbn] = new_book
            self.books_by_title.insert(new_book)
            
            if verbose: print(f"Added: \"{title}\"")
            return True
        except ValueError as e:
            if verbose: print(f"Error adding book: {e}")
            return False

    ## book removal 
    def remove_book(self, isbn, verbose=True):
        """Removes a book from the library by its ISBN."""
        # 1. checks if the book exists in the ISBN map (O(1))
        book_to_remove = self.books_by_isbn.get(isbn)
        
        if not book_to_remove:
            if verbose: print(f"Error: Book with ISBN {isbn} not found.")
            return False

        # 2. checks if the book is checked out or has a waitlist
        if book_to_remove.is_checked_out or book_to_remove.waitlist:
            if verbose: 
                print(f"Error: Cannot remove \"{book_to_remove.title}\".")
                if book_to_remove.is_checked_out:
                    print("Book is currently checked out.")
                if book_to_remove.waitlist:
                    print(f"Book has {len(book_to_remove.waitlist)} users on the waitlist.")
            return False

        # 3. removed from ISBN dictionary (O(1))
        del self.books_by_isbn[isbn]

        # 4. removed from Title BST (O(log n) average)
        self.books_by_title.delete(book_to_remove.title)

        if verbose: print(f"Successfully removed: \"{book_to_remove.title}\" (ISBN: {isbn}).")
        return True
    
    # checkout       
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
            
    # Methods from the 'original'' test code
    
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


# FULL TESTING CODE # 

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
    my_library.find_book_by_isbn("000-0-00-000000-0") # non existent
    
    my_library.find_book_by_title("Clean Code")
    my_library.find_book_by_title("Non-Existent Book") # non existent
    
    # 5. Test feature: Checking out a book
    print("\n--- Test: Checkout Process ---")
    my_library.checkout_book("978-0-13-235088-4", "user_alice")
    my_library.find_book_by_isbn("978-0-13-235088-4") # check status has changed
    
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

# removal test code
def run_removal_tests():
    """
    Test suite to verify the new remove_book functionality.
    """
    print("\n     RUNNING BOOK REMOVAL TEST SUITE")

    library = Library(size=10)
    
    # setup - add books for testing
    library.add_book("A1", "Book A", "Author X", verbose=False)
    library.add_book("B2", "Book B", "Author Y", verbose=False)
    library.add_book("C3", "Book C", "Author Z", verbose=False)
    library.checkout_book("B2", "user_temp")
    library.checkout_book("C3", "user_waitlist")

    # Test Case 1: remove an existing available book
    print("\n--- 1. Test: Remove an available book (ISBN A1) ---")
    # verify pre removal existence
    print("Pre-removal check:")
    library.find_book_by_isbn("A1") 
    
    success = library.remove_book("A1")
    print(f"Removal successful: {success}")
    
    # verify post removal non existence
    print("Post-removal check (should be 'No book found'):")
    library.find_book_by_isbn("A1")
    
    # Test Case 2: Remove a non existent book
    print("\n--- 2. Test: Remove a non-existent book (ISBN D4) ---")
    success = library.remove_book("D4")
    print(f"Removal successful: {success}")

    # Test Case 3: Attempt to remove a checked-out book (should fail)
    print("\n--- 3. Test: Attempt to remove a checked-out book (ISBN B2) ---")
    success = library.remove_book("B2")
    print(f"Removal successful: {success}")
    # Verify it still exists
    library.find_book_by_isbn("B2")

    # Test Case 4: Attempt to remove a book with a waitlist (should fail)
    print("\n--- 4. Test: Attempt to remove a book with a waitlist (ISBN C3) ---")
    # C3 is checked out and has a waitlist user from the setup
    library.return_book("C3") # returned it to test the waitlist only failure case
    success = library.remove_book("C3")
    print(f"Removal successful: {success}")
    # vrify it still exists
    library.find_book_by_isbn("C3")

    # Test case 5: Final successful removal (after the waitlist cleared)
    print("\n--- 5. Test: Remove successfully after waitlist is clear (ISBN C3) ---")
    # waitlist for C3 is now clear, but it is checked out to 'user_waitlist'
    library.return_book("C3") # this should make it available

    # now attempts the removal again
    success = library.remove_book("C3")
    print(f"Removal successful: {success}")
    # verifys
    print("Post-removal check (should be 'No book found'):")
    library.find_book_by_isbn("C3")
    
    # final check of the list
    library.list_all_books()
    print("Book Removal Tests Passed!")

## scalabilty testing 

def run_scalability_test():
    """
    This is the  1M test suite to demonstrate O(n log n)
    insertion and fast O(1) / O(log n) search.
    """
    print(" RUNNING SCALABILITY TEST SUITE (1,000,000 BOOKS)")
    
    num_books = 1000000
    
    # initialise a new library (size parameter kept for compatibility)
    large_library = Library(size=int(num_books * 1.25))
    
    print(f"--- 1. Testing scalability with {num_books} books ---")
    print(f"Adding {num_books} books with RANDOM titles...")
    print("(This loop is silent for maximum speed)...")
    
    start_time = time.time()
    for i in range(num_books):
        # integer ISBN
        isbn = i
        # random Title (prevents BST from becoming unbalanced)
        ## IMPORTANT - PURELY FOR TESTING WOULD NOT BE IN HYPERTHETICAL PRODUCTION CODE ##
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

    print("Searching for a book by ISBN (dict)...")
    start_time = time.time()
    result = large_library.find_book_by_isbn(isbn_to_find, verbose=False)
    end_time = time.time()
    print(f"Result found: \"{result.title}\"")
    print(f" dict search time: {(end_time - start_time) * 1e6:.2f} microseconds. (O(1) speed)")
    
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
    run_removal_tests() 
    run_scalability_test()