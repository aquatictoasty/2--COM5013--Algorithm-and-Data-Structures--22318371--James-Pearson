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