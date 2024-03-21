from LinkedList import *
from Node import *

n1 = Node("Node 1")
n2 = Node("Node 2")
n3 = Node("Node 3")
n4 = Node("Node 4")
ll = LinkedList()
ll.append(n1)
ll.append(n2)
ll.append(n3)
ll.append(n4)
ll.printList()
print(40*"+")
ll.printRev()
print(40*"+")
ll.nodePointers("Node 3")