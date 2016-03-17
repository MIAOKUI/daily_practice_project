from myNode import Node
from myStack import Stack
class Tree:
    def __init__(self, value):
        self.root = Node(value)
    def add_left(self, tree):
        self.root.left = tree
    def add_right(self, tree):
        self.root.right = tree
    @property
    def left(self):
        return(self.root.left)
    @property
    def right(self):
        return(self.root.right)

    def visit_first(self,fn):
        fn(self.root.value)
        if self.left:
            self.left.visit_first(fn)
        if self.right:
            self.right.visit_first(fn)


    def iter_visit_first(self,fn):
        stack = Stack()
        stack.push(self)
        while stack.top:
            s = stack.pop()
            fn(s.root.value)
            if s.right:
                stack.push(s.right)
            if s.left:
                stack.push(s.left)

    def iter_visit_middel(self,fn):
        stack = Stack()
        isLeaf = self.left is None and self.right is None
        if not isLeaf:
            if self.right:
                stack.push(self.right)

            stack.push(self)

            if self.left:
                stack.push(self.left)

        while stack.top:
            s = stack.pop()
            if s is self:
                fn(s.root.value)
                s = stack.pop()
            isLeaf = s.left is None and s.right is None
            if not isLeaf:
                if s.right:
                    stack.push(s.right)
                stack.push(s)
                if s.left:
                    stack.push(s.left)
            else:
                fn(s.root.value)
                if stack.top:
                    fn(stack.pop().root.value)

    def iter_visit_last(self,fn):
        stack = Stack()
        isLeaf = self.left is None and self.right is None
        if not isLeaf:
            stack.push(self)
            if self.right:
                stack.push(self.right)
            if self.left:
                stack.push(self.left)

        while stack.top:
            s = stack.pop()
            if s is self:
                fn(s.root.value)
                continue
            isLeaf = s.left is None and s.right is None
            if not isLeaf:
                stack.push(s)
                if self.right:
                    stack.push(s.right)
                if self.left:
                    stack.push(s.left)
            else:
                fn(s.root.value)
                fn(stack.pop().root.value)
                fn(stack.pop().root.value)










    def visit_middle(self,fn):
        if self.left:
            self.left.visit_middle(fn)
        fn(self.root.value)
        if self.right:
            self.right.visit_middle(fn)
    def visit_last(self, fn):
        if self.left:
            self.left.visit_last(fn)
        if self.right:
            self.right.visit_last(fn)
        fn(self.root.value)


if __name__ == '__main__':
    d = Tree('D')
    e = Tree('E')
    f = Tree('F')
    g = Tree('G')

    b = Tree('B')
    b.add_left(d)
    b.add_right(e)

    c = Tree('C')
    c.add_left(f)
    c.add_right(g)

    a = Tree('A')
    a.add_left(b)
    a.add_right(c)
    a.iter_visit_last(print)