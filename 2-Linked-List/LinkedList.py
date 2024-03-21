# Todo:

#  - def NodePointers(data): ## Search for data first
#       print(data.next)
#       print(data.prev)


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def getList(self):
        all_items = []
        temp = self.head
        temp_str = f"Data: {temp.getData()}\nNext: {temp.getNext()}\nPrev: {temp.getPrev()}"
        all_items.append(temp_str)
        while temp.next:
            temp = temp.next
            temp_str = f"Data: {temp.getData()}\nNext: {temp.getNext()}\nPrev: {temp.getPrev()}"
            all_items.append(temp_str)
        return all_items


    def getLength(self):
        if self.head == None:
            return 0
        else:
            temp = self.head
            length = 1
        while temp.next:
            temp = temp.next
            length += 1
        return length

    def printList(self):
        ll = self.getList()
        for i in ll:
            print(30*'-')
            print(i)
        print(30*'-')

    def printRev(self):
        ll = self.getList()
        ll.reverse()
        for i in ll:
            print(30*'-')
            print(i)
        print(30*'-')

    def append(self, new_node):
        if self.head is None:
            self.head = new_node
            return
        temp_node = self.head
        while temp_node.next:
            temp_node = temp_node.next
        temp_node.next = new_node
        temp_node.next.prev = temp_node

    def nodePointers(self, data):
        temp_node = self.head
        while temp_node.data != data:
            temp_node = temp_node.next
        print("Next data: " + temp_node.next.data)
        print("Prev data: " + temp_node.prev.data)
