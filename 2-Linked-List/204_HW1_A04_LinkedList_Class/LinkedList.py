#!/usr/bin/env python3
"""Linked List -> Extended Linked List Implementation: Homework

The goal of this homework is to implement a singly linked list data structure with additional functionalities.
In previous tutorials you have learned how a node and a linked list data structure in its basic form can be created.
However, a LinkedList class can have more methods to perform additional operations on a linked list,
such as: insertion (begin, end, or after a specific element), deletion, traversal, and sorting.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code
    * run the test of this homework located in same folder.

To test run LinkedList_t.py in your command line'

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on linked list:
    https://realpython.com/linked-lists-python/
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    #TODO 1: Insert at the beginning of the list
    def insertBeg(self, new_data):
        temp_node = self.head
        self.head = Node(new_data)
        self.head.next = temp_node

    #TODO 2: Insert at the end
    def insertEnd(self, new_data):
        new_node = Node(new_data)
        if self.head is None:
            self.head = new_node
            return

        temp_node = self.head
        while temp_node.next:
            temp_node = temp_node.next
        temp_node.next = new_node

    #TODO 3: Insert after a specific node
    def insertAfter(self, data, new_data):
        new_node = Node(new_data)
        temp_node = self.head
        while temp_node.data != data:
            temp_node = temp_node.next
        new_node.next = temp_node.next
        temp_node.next = new_node

    #TODO 4: Deleting a node at a specific index
    def deleteIndex(self, index):
        if index == 0:
            self.head = self.head.next
            return
        temp_node = self.head
        counter = 0
        while counter < index-1:
            temp_node = temp_node.next
            counter += 1
        temp_node.next = temp_node.next.next


    #TODO 5: Search an element
    def find(self, key):
        temp_node = self.head
        i = 0
        while temp_node.next:
            if temp_node.data == key:
                return i
            temp_node = temp_node.next
            i += 1
        return -1

    #TODO 6: Sort the linked list
    def sort(self, head):
        temp_node = self.head
        new_list = [temp_node.data]
        while temp_node.next:
            temp_node = temp_node.next
            new_list.append(temp_node.data)

        new_list.sort()

        new_head = Node(new_list[0])
        temp_node = new_head
        i = 1
        while i < len(new_list):
            temp_node.next = Node(new_list[i])
            temp_node = temp_node.next
            i+=1
        self.head = new_head


    #TODO 7: Print the linked list
    def printList(self):
        temp_node = self.head
        print(f"Head: {temp_node.data}")
        node_counter = 1
        while temp_node.next:
            temp_node = temp_node.next
            print(f"Node {node_counter}: {temp_node.data}")
            node_counter += 1