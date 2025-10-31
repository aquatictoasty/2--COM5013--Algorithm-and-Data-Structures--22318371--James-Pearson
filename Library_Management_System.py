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