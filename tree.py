from _token  import *
from nodes   import *

def tree(node, indent = "", isLast = True):

    pointer = "└─"   if isLast else "├─"

    print(f'{indent}{pointer}', end = "")

    indent += "    " if isLast else "│   "

    try:
        tree_     = node.tree()
        lastChild = tree_[len(tree_) - 1]

    except AttributeError: print(node); return

    if  isinstance(node, Token)                  or \
        isinstance(node, IfNode)                 or \
        isinstance(node, IntNode)                or \
        isinstance(node, ForNode)                or \
        isinstance(node, GetNode)                or \
        isinstance(node, SetNode)                or \
        isinstance(node, CallNode)               or \
        isinstance(node, ListNode)               or \
        isinstance(node, BinOpNode)              or \
        isinstance(node, BreakNode)              or \
        isinstance(node, WhileNode)              or \
        isinstance(node, ReturnNode)             or \
        isinstance(node, StringNode)             or \
        isinstance(node, UnaryOpNode)            or \
        isinstance(node, ForEachNode)            or \
        isinstance(node, TernaryNode)            or \
        isinstance(node, VariableNode)           or \
        isinstance(node, ContinueNode)           or \
        isinstance(node, VariableAccessNode)     or \
        isinstance(node, FunctionDefinitionNode)    \
        : print(node.__class__.__name__)

    for child in tree_: tree(child, indent, child == lastChild)