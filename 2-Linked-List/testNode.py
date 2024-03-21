from Node import *
E = Node("E")
B = Node("B")
A = Node("A", B)
C = Node("C", A)
B.setNext(E)
print(B.getNext())
print(B.getData())
