class Ring:
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.size = size
        self.__counter = 0

    def append(self,node):
        if self.__counter == 0:
            self.head = node
            self.tail = node
            self.__counter +=1
        elif self.__counter < self.size:
            self.tail.next = node
            self.tail = node
            self.__counter += 1
        else:
            self.head = self.head.next
            self.tail.next = node
            self.tail = node

    def pop(self):
        if self.__counter > 1:
            oldHead = self.head
            self.head = self.head.next
            self.__counter -= 1
            return(oldHead.value)
        elif self.__counter == 1:
            oldHead = self.head
            self.head = None
            self.tail = None
            self.__counter -= 1
            return(oldHead.value)
        else:
            raise Exception('Emtpy ring')