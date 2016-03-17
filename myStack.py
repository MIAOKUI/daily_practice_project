from myNode import Node
class Stack:
    def __init__(self):
        self.top = None
        self.next = None
    def push(self, value):
        node = Node(value)
        if not self.top:
            self.top = node
        else:
            node.next = self.top
            self.top = node
    def pop(self):
        if self.top:
            node = self.top
            self.top = self.top.next
            return(node.value)
        else:
            raise Exception('Empty stack')