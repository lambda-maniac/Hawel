class IntNode:
    def __init__(self, token):
        self.token = token

        self.token.value = int(self.token.value)

    def tree(self):
        return [self.token]
        
class StringNode:
    def __init__(self, token):
        self.token = token

        self.token.value = self.token.value[1:-1:]

    def tree(self):
        return [self.token]

class UnaryOpNode:
    def __init__(self, operator, node):
        self.operator = operator
        self.node     = node

    def tree(self):
        return [self.operator, self.node]

class VariableNode:
    def __init__(self, name, valueNode):
        self.name      = name
        self.valueNode = valueNode

    def tree(self):
        return [self.name, self.valueNode]

class VariableAccessNode:
    def __init__(self, variable):
        self.variable = variable

    def tree(self):
        return [self.variable]

class GetNode:
    def __init__(self, node, slicesNodes):
        self.node        = node
        self.slicesNodes = slicesNodes

    def tree(self):
        return [ListNode(self.slicesNodes), self.node]

class SetNode:
    def __init__(self, node, indexNode, valueNode):
        self.node      = node
        self.indexNode = indexNode
        self.valueNode = valueNode

    def tree(self):
        return [self.node, self.indexNode, self.valueNode]

class BinOpNode:
    def __init__(self, operation, leftNode, rightNode):
        self.operation = operation
        self.leftNode  = leftNode
        self.rightNode = rightNode

    def tree(self):
        return [self.leftNode, self.operation, self.rightNode]

class TernaryNode:
    def __init__(self, condition, caseTrueNode, caseFalseNode):
        self.condition     = condition
        self.caseTrueNode  = caseTrueNode
        self.caseFalseNode = caseFalseNode

    def tree(self):
        return [self.condition, self.caseTrueNode, self.caseFalseNode]

class IfNode:
    def __init__(self, cases):
        self.cases = cases

    def tree(self):
        cases = []
        for condition, expression in self.cases:
            cases.append(condition)
            cases.append(expression)
        return cases

class ForNode:
    def __init__(self, variableNameToken, startValueNode, endValueNode, stepValueNode, bodyNode):
        self.variableNameToken = variableNameToken
        self.startValueNode    = startValueNode
        self.endValueNode      = endValueNode
        self.stepValueNode     = stepValueNode
        self.bodyNode          = bodyNode

    def tree(self):
        return [self.variableNameToken, self.startValueNode, self.endValueNode, self.stepValueNode, self.bodyNode]

class ForEachNode:
    def __init__(self, variableNameToken, iterableNode, bodyNode):
        self.variableNameToken = variableNameToken
        self.iterableNode      = iterableNode
        self.bodyNode          = bodyNode

    def tree(self):
        return [self.variableNameToken, self.iterableNode, self.bodyNode]

class WhileNode:
    def __init__(self, conditionNode, bodyNode):
        self.conditionNode = conditionNode
        self.bodyNode      = bodyNode

    def tree(self):
        return [self.conditionNode, self.bodyNode]

class FunctionDefinitionNode:
    def __init__(self, functionNameToken, argNameTokens, bodyNode):
        self.functionNameToken = functionNameToken
        self.argNameTokens     = argNameTokens
        self.bodyNode          = bodyNode

    def tree(self):
        return [self.functionNameToken, self.argNameTokens, self.bodyNode]

class ReturnNode:
    def __init__(self, nodeToReturn):
        self.nodeToReturn = nodeToReturn

    def tree(self):
        return [self.nodeToReturn]

class ContinueNode:
    def __init__(self): pass
    def tree(self)    : return ["continue"]

class BreakNode:
    def __init__(self): pass
    def tree(self)    : return ["break"]

class CallNode:
    def __init__(self, nodeToCall, argNodes):
        self.nodeToCall = nodeToCall
        self.argNodes   = argNodes

    def tree(self):
        return [self.nodeToCall, ListNode(self.argNodes)]

class ListNode:
    def __init__(self, nodeList):
        self.nodeList = nodeList

    def tree(self):
        return [node for node in self.nodeList]