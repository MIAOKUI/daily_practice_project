from myStack import Stack
import re
from myTree import Tree

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


def treeParser(parsedExpress):
    """

    :rtype: object
    """
    stack = Stack()
    for item in parsedExpress:
        if item == '(':
            stack.push(item)
        elif item == ')':
            st = stack.pop()
            if stack.pop() != '(':
                raise Exception('Bracket not compatible ')
            stack.push(st)
        elif item in '&|':
            tree = Tree(item)
            st = stack.pop()
            if st  == '(':
                raise Exception('Binary operator not compatible')
            tree.add_left(st)
            stack.push(tree)
        elif item == '!':
            stack.push(Tree(item))
        else:
            st = stack.pop()
            if st == '(':
                stack.push(st)
                stack.push(Tree(item))
            else:
                st.add_right(Tree(item))
                stack.push(st)

    tree = stack.pop()
    while stack.top:
        st = stack.pop()
        st.add_right(tree)
        if not stack.top:
            return(st)
        tree = st


def callback(line, expr):
    if expr in '&|!':
        return(expr)
    else:
        return re.search(expr, line) is not None


def treeMatch(exprTree,line,fn):
    if exprTree.root.value == '!':
        if exprTree.left:
            raise Exception('Unary operation do not have left child')
        if not exprTree.right:
            raise Exception('Unary operation do not have right child')
        return(treeMatch(exprTree.right, line , fn))

    elif exprTree.root.value in '|&':
        if not exprTree.left:
            raise Exception('Binary operation unbalanced: cannot find left child')
        if not exprTree.right:
            raise Exception('Binary operation unbalanced: cannot find right child')

        if exprTree.root.value == '|':
           return treeMatch(exprTree.left, line, fn) or treeMatch(exprTree.right, line, fn)
        if exprTree.root.value == '&':
           return treeMatch(exprTree.left, line, fn) and treeMatch(exprTree.right, line, fn)
    else:
        return fn(line,exprTree.root.value)




def match(exprsGroup, line, fn):
    exprT = tokenizer(exprsGroup)
    exprP = exprParser(exprT)
    parsedTree = treeParser(exprP)
    return( treeMatch(parsedTree,line,fn))


if __name__ == '__main__':
    print(match('(#e3# | #e2#) |(!#e3# & #e4#)', 'e1aaaaaae2', callback) )


