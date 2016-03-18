from myNode import Node
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

# (#e1# & #e2#) |(!#e3# & #e4#)




# def match(line, exprs, fn):
#     exprsTokens = tokenizer(exprs)
#     exprsParsed = exprParser(exprsTokens)
#     stack = Stack()
#     for expr in exprsParsed:
#         if expr in '(!|&':
#             stack.push(expr)
#         else:
#             if expr != ')':
#                 v = fn(line, expr)
#                 s = stack.pop()
#                 if s == '!':
#                     v = not v
#                     stack.push(v)
#                 elif s == '&':
#                     v2 = stack.pop()
#                     if isinstance(v2, bool):
#                         v = v and v2
#                         stack.push(v)
#                     else:
#                         raise Exception('Wrong expression')
#                 elif s == '|':
#                     v2 = stack.pop()
#                     if isinstance(v2, bool):
#                         v = v and v2
#                         stack.push(v)
#                     else:
#                         raise Exception('Wrong expression')
#                 elif s == '(':
#                     stack.push(v)
#                 else:
#                     raise Exception('Wrong expression')
#             else:
#                 v = stack.pop()
#                 print(v)
#                 if not isinstance(v, bool):
#                     raise Exception('No express in brackets')
#
#                 stack.push(v)
#     return(stack.top.value)


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


#match('e1aaaaaae2', '(#e1# | #e2#) |(!#e3# & #e4#)', callback)

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


def match(exprTree, line, fn):
    stack = Stack()
    while stack.top:
        st = stack.pop()
        if st.root.value in '&|':
            if st.right:
                stack.push(st.right)
            else:
                raise Exception('Unbalanced binary operation!')

            if st.left:
                stack.push(st.right)
            else:
                raise Exception('Unbalanced binary operation!')
            stack.push(st)

        elif st.root.value == '!':
            if st.right:
                stack.push(st.right)
            elif st.left:
                raise Exception('Unary operation cannot have left node')
            else:
                raise Exception('No unary operation leaf')

        else:
            if stack.top:
                st2 = stack.pop()
                if st2 == '!':
                    st = not st
                    stack.push(st)
                else:
                    if st2 in '&|!':
                        raise Exception('Wrong operation')
                    else:
                        op = stack.pop()
                        if op == '&':
                            st = st and st2
                            stack.push(st)
                        elif op == '|':
                            st = st or st2
                            stack.push(st)
                        else:
                            raise Exception('Wrong operation')
            else:
                return(st)








exprT = tokenizer('(#e1# & #e2#) |(!#e3# & #e4#) & (!#e5# & #e6#)')
#for item in exprT:
#    print(item.value,item.isExpr)


exprP = exprParser(exprT)
#print(exprP)
parsedTree = treeParser(exprP)

# def a(item):
#     return(item)
# parsedTree.visit_first(a)
