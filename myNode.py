class Node:
    def __init__(self,value):
        self.value = value
        self.next = None
        self.left = None
        self.right = None
    def getValue(self):
        return(self.value)