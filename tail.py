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


class Token:
    def __init__(self, value,isExpr):
        self.value = value
        self.isExpr = isExpr


def tokenizer(exprs):
    exprToken = []
    cIdx = 0
    isExpr = False
    for c in exprs:
        if c == '#':
            isExpr = not isExpr
        elif c in '()!&':
            exprToken.append(Token(c, isExpr))
        elif c.strip() == '':
            continue
        else:
            exprToken.append(Token(c, isExpr))
    if isExpr:
        raise Exception('Wrong expression')
    return exprToken



def exprParser(exprToken):
    expr = []
    cellExpr = ''
    for token in exprToken:
        if token.isExpr:
            cellExpr += token.value
        else:
            if cellExpr:
                expr.append(cellExpr)
                cellExpr = ''
            expr.append(token.value)
    if cellExpr:
        expr.append(cellExpr)
    return(expr)

# (#e1# & #e2#) |(!#e3# & #e4#)

def callback(line, expr):
    return re.search(expr, line) is not None


def match(line, exprs, fn):
    exprsTokens = tokenizer(exprs)
    exprsParsed = exprParser(exprsTokens)
    stack = Stack()
    for expr in exprsParsed:
        if expr in '(!|&':
            stack.push(expr)
        else:
            if expr != ')':
                v = fn(line, expr)
                s = stack.pop()
                if s == '!':
                    v = not v
                    stack.push(v)
                elif s == '&':
                    v2 = stack.pop()
                    if isinstance(v2, bool):
                        v = v and v2
                        stack.push(v)
                    else:
                        raise Exception('Wrong expression')
                elif s == '|':
                    v2 = stack.pop()
                    if isinstance(v2, bool):
                        v = v and v2
                        stack.push(v)
                    else:
                        raise Exception('Wrong expression')
                elif s == '(':
                    stack.push(v)
                else:
                    raise Exception('Wrong expression')
            else:
                v = stack.pop()
                print(v)
                if not isinstance(v, bool):
                    raise Exception('No express in brackets')

                stack.push(v)
    return(stack.top.value)


    # while stack.top:
    #     v1 = stack.pop()
    #     if not isinstance(v1, bool):
    #         raise Exception('Wrong expression')
    #     s = stack.pop()
    #     if s == '!':
    #         v1 = not v1
    #     elif s == '&':
    #         v2 = stack.pop()
    #         if not isinstance(v2,bool):
    #             raise Exception('Wrong expression')
    #         v1 = v1 and v2
    #     elif s == '|':
    #         v2 = stack.pop()
    #         if not isinstance(v2, bool):
    #             raise Exception('Wrong expression')
    #         v1 = v1 or v2
    #     else:
    #         pass
    #         #raise Exception('Wrong expression')
    #     stack.push(v1)
    # else:
    #     return(stack.top)


match('e1aaaaaae2', '(#e1# | #e2#) |(!#e3# & #e4#)', callback)




exprT = tokenizer('(#e1# & #e2#) |(!#e3# & #e4#)')
#for item in exprT:
#    print(item.value,item.isExpr)


exprP = exprParser(exprT)
#print(exprP)









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


