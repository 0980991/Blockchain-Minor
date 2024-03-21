class Node:
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self):
        return "Object{" + self.data + "}"

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getNext(self):
        return self.next

    def setNext(self, node):
        self.next = node

    def getPrev(self):
        return self.prev

    def setPrev(self, node):
        self.prev = node