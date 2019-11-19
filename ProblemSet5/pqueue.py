# File: pqueue.py

"""
This module implements the priority queue abstraction using a heap to
represent a partially ordered tree in which every node is smaller
than either of its children.  Maintaining this property during add
and remove operations requires log N time.
"""

class PriorityQueue:
    """
    This class implements a queue structure whose elements are
    removed in priority order.  As in conventional English usage,
    lower priority values are removed first.  Thus, priority 1
    items come before priority 2.
    """

    def __init__(self):
        """Creates an empty priority queue."""
        self.capacity = PriorityQueue.INITIAL_CAPACITY
        self.array = [ None ] * self.capacity
        self.count = 0
        self.timestamp = 0

    def size(self):
        """Returns the number of values in this queue."""
        return self.count

    def isEmpty(self):
        """Returns True if this queue contains no elements."""
        return self.count == 0

    def clear(self):
        """Removes all elements from this queue."""
        self.count = 0

    def enqueue(self, value, priority=0):
        """Adds value to this queue using the specified priority."""
        if self.count == self.capacity:
            self.expandCapacity()
        array = self.array
        index = self.count
        self.count += 1
        self.timestamp += 1
        entry = PriorityQueue.PQEntry(value, priority, self.timestamp)
        self.array[index] = entry
        while index > 0:
            parent = (index - 1) // 2
            if array[parent] < array[index]:
                break
            array[parent],array[index] = array[index],array[parent]
            index = parent

    def dequeue(self):
        """Removes the first element from this queue and returns it."""
        return dequeueWithPriority(self)[0]

    def dequeueWithPriority(self):
        """Dequeues a tuple of the first element and its priority."""
        if self.count == 0:
            raise IndexError("dequeue called on an empty queue")
        array = self.array
        pair = (array[0].value, array[0].priority)
        self.count -= 1
        array[0] = array[self.count]
        index = 0
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            if left >= self.count:
                break
            child = left
            if right < self.count and array[right] < array[left]:
                child = right
            if array[index] < array[child]:
                break
            array[child],array[index] = array[index],array[child]
            index = child
        return pair

    def peek(self):
        """Returns the first item in the queue without removing it."""
        if self.count == 0:
            raise IndexError("peek called on an empty queue")
        return self.array[0].value

    def peekPriority(self):
        """Returns the priority of the first item in the queue."""
        if self.count == 0:
            raise IndexError("peekPriority called on an empty queue")
        return self.array[0].priority

# Implementation notes: expandCapacity
# ------------------------------------
# The expandCapacity method allocates a array of twice the previous
# size, copies the old elements to the array, and then replaces the
# old array with the one.

    def expandCapacity(self):
        self.capacity *= 2
        newArray = [ None ] * self.capacity
        for i in range(self.count):
            newArray[i] = self.array[i]
        self.array = newArray

# Constants

    INITIAL_CAPACITY = 10

# Implementation notes: PQEntry
# -----------------------------
# This private class combines three values: a value, a priority,
# and a timestamp.  The timestamp is used to break ties between
# items of equal priority and therefore ensures that such items
# obey the standard first-in/first-out queue discipline.  This
# class implements the less-than operator to simplify priority
# comparisons.

    class PQEntry:
        def __init__(self, value, priority, timestamp):
            self.value = value
            self.priority = priority
            self.timestamp = timestamp
        def __lt__(self, other):
            if self.priority < other.priority:
                return True
            if self.priority > other.priority:
                return False
            return self.timestamp < other.timestamp
