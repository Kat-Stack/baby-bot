# A single node of a singly linked list
class Node:
  # constructor
  def __init__(self, data = None, next=None): 
    self.data = str(data)
    self.next = next

# A Linked List class with a single head node
class LinkedList:
  def __init__(self):  
    self.head = None
  
  # insertion method for the linked list
  def insert(self, data):
    newNode = data
    if(self.head):
      current = self.head
      while(current.next):
        current = current.next
      current.next = newNode
    else:
      self.head = newNode

  
  # print method for the linked list
  def printLL(self):
    current = self.head
    while(current):
      print(current.data)
      current = current.next

  # return the results of the linked list
  def getLL(self):
    current = self.head
    response = ""
    while(current):
      response += current.data + " "
      current = current.next
    return response

    #travels up the linkedNode and returns a sequence of linkedNodes (ex: I am K -> I, I am, I am K)
  def printBackwards(self, collection=[]):
    current = self.head
    collection.append(self)
    while(current):
      current = current.next
    return collection




# Singly Linked List with insertion and print methods
#LL = LinkedList()
#LL.insert(3)
#LL.insert(4)
#LL.insert(5)
#LL.printLL()