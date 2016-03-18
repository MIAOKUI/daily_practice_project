#!/usr/bin/env python3.4
#
import sys, optparse, time,re

class Node:
    def __init__(self,value):
        self.value = value
        self.next = None
    def getValue(self):
        return(self.value)


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











def main():
    optParse = optparse.OptionParser( usage = 'tail.py [options] <file>')
    optParse.add_option('-s',"--size",type = 'int', dest = 'lines', default = 10)
    opts, args = optParse.parse_args()

    if len( sys.argv ) == 1:
        optParse.print_help()
        sys.exit(1)
    input = args[0]
    ring = Ring(opts.lines)
    cPos = 0
    while True:
        with open(input,'r') as f:
            f.seek(cPos)
            line = f.readline()
            while line:
                ring.append(Node(line))
                line = f.readline()
            else:
                cPos = f.tell()
                while ring.head:
                   print(ring.pop().strip())
        time.sleep(5)



# if __name__ == '__main__':
#     main()


