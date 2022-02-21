# Name: Matthew Norwood
# OSU Email: norwooma@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3/21
# Description: The program file contains code that implements a hash_map data
# structure. It leverages both of the previously defined LinkedList and
# DynamicArray classes which were derived in earlier assignments.


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        This method takes each bucket and replaces it with a new LinkedList, effectively resetting the data structure.
        """
        for index in range(0, self.buckets.length()):
            self.buckets.set_at_index(index, LinkedList())
        self.size = 0
        return

    def get(self, key: str) -> object:
        """
        TODO: Write this implementation
        """
        for index in range(0, self.buckets.length()):
            current_LL = self.buckets.get_at_index(index)
            if current_LL.contains(key):
                cur = current_LL.head
                while cur is not None:
                    if cur.key == key:
                        return cur.value
                    cur = cur.next

        return None

    def put(self, key: str, value: object) -> None:
        """
        TODO: Write this implementation
        """

        # first, search for nonempty buckets

        # i use one variable for the index and another for the count of
        # iterations so we know when to stop searching.
        index = 0

        while index < self.buckets.length():
            # the current bucket is a LL object, so check if the head is
            # not None
            current_bucket = self.buckets.get_at_index(index)
            if current_bucket.head is not None:
                if current_bucket.contains(key):
                    current_bucket.remove(key)
                    current_bucket.insert(key, value)
                    return
            index += 1

        hashed_key = self.hash_function(key)
        # if the key wasn't present in the HashMap, add it and its value
        index = hashed_key % self.buckets.length()
        current_bucket = self.buckets.get_at_index(index)
        current_bucket.insert(key, value)
        self.size += 1
        return

    def remove(self, key: str) -> None:
        """
        TODO: Write this implementation
        """
        for index in range(0, self.buckets.length()):
            current_LL = self.buckets.get_at_index(index)
            if current_LL.contains(key):
                current_LL.remove(key)
                self.size -= 1
                return

        return None

    def contains_key(self, key: str) -> bool:
        """
        TODO: Write this implementation
        """
        for index in range(0, self.buckets.length()):
            current_LL = self.buckets.get_at_index(index)
            if current_LL.contains(key):
                return True
        return False

    def empty_buckets(self) -> int:
        """
        TODO: Write this implementation
        """

        # *** IMPLEMENT PUT THEN TEST ***
        i = 0
        empty_count = 0
        while i < self.buckets.length():
            current_bucket = self.buckets.get_at_index(i)
            if current_bucket.length() == 0:
                empty_count += 1
            i += 1
        return empty_count

    def table_load(self) -> float:
        """
        TODO: Write this implementation
        """
        # load factor (lambda) = number of elements stored in the table / number
        # of buckets

        # get the length of each LinkedList and sum the lengths to get the
        # number of elements.
        element_count = 0
        for index in range(0, self.buckets.length()):
            currentLL = self.buckets.get_at_index(index)
            element_count += currentLL.length()

        if self.buckets.length != 0:
            load_factor = float(element_count / self.buckets.length())
            return load_factor
        else:
            return 0.0

    def resize_table(self, new_capacity: int) -> None:
        """
        TODO: Write this implementation
        """
        if new_capacity < 1:
            return None

        new_hash = HashMap(new_capacity, self.hash_function)

        for index in range(0, self.buckets.length()):
            current_ll = self.buckets.get_at_index(index)
            current_ll_node = current_ll.head
            while current_ll_node is not None:
                new_hash.put(current_ll_node.key, current_ll_node.value)
                current_ll_node = current_ll_node.next

        self.buckets = new_hash.buckets
        self.size = new_hash.size
        self.capacity = new_hash.capacity

    def get_keys(self) -> DynamicArray:
        """
        TODO: Write this implementation
        """
        key_array = DynamicArray()
        for index in range(0, self.buckets.length()):
            current_ll = self.buckets.get_at_index(index)
            current_ll_node = current_ll.head
            while current_ll_node is not None:
                key_array.append(current_ll_node.key)
                current_ll_node = current_ll_node.next

        return key_array

# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")

    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
