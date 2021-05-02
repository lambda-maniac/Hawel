class IntNode:
    def __init__(self, token):
        self.token = token

        self.token.value = int(self.token.value)

    def __repr__(self):
        return str(
            {
                "int": {
                    "value": self.token.value
                }
            }
        )

class StringNode:
    def __init__(self, token):
        self.token = token

        self.token.value = self.token.value[1:-1:]

    def __repr__(self):
        return str(
            {
                "string": {
                    "value": self.token.value
                }
            }
        )

class UnaryOpNode:
    def __init__(self, operator, node):
        self.operator = operator
        self.node     = node

    def __repr__(self):
        return str(
            {
                "UnaryOperation": {
                    "operation": self.operator.type,
                    "nodeToOperate": self.node
                }
            }
        )

class VariableNode:
    def __init__(self, name, valueNode):
        self.name      = name
        self.valueNode = valueNode

    def __repr__(self):
        return str(
            {
                "set": {
                    "name": self.name,
                    "to": self.valueNode
                }
            }
        )

class VariableAccessNode:
    def __init__(self, variable):
        self.variable = variable

    def __repr__(self):
        return str(
            {
                "get": {
                    "name": self.variable.value
                }
            }
        )

class GetNode:
    def __init__(self, node, slicesNodes):
        self.node        = node
        self.slicesNodes = slicesNodes

    def __repr__(self):
        return str(
            {
                "of": self.node,
                "get": {
                    "from": self.slicesNodes[0],
                    "to": self.slicesNodes[1]
                }
            }
        )

class SetNode:
    def __init__(self, node, indexNode, valueNode):
        self.node      = node
        self.indexNode = indexNode
        self.valueNode = valueNode

    def __repr__(self):
        return str(
            {
                "of": self.node,
                "set": {
                    "index": self.indexNode,
                    "to": self.valueNode
                }
            }
        )

class BinOpNode:
    def __init__(self, operation, leftNode, rightNode):
        self.operation = operation
        self.leftNode  = leftNode
        self.rightNode = rightNode

    def __repr__(self):
        return str(
            {
                "BinaryOperation": {
                    "operation": self.operation.type,
                    "operateOn": {
                        "left": self.leftNode,
                        "right": self.rightNode
                    }
                }
            }
        )

class IfNode:
    def __init__(self, cases):
        self.cases = cases

    def __repr__(self):

        ifDict = {"if": {}}; n = 0
        for condition, expression in self.cases:
            ifDict["if"][f"if_{str(n).zfill(3)}"] = {
                "condition": condition,
                "do": expression
            }
            n += 1

        return str(ifDict)

class ForNode:
    def __init__(self, variableNameToken, startValueNode, endValueNode, stepValueNode, bodyNode):
        self.variableNameToken = variableNameToken
        self.startValueNode    = startValueNode
        self.endValueNode      = endValueNode
        self.stepValueNode     = stepValueNode
        self.bodyNode          = bodyNode

    def __repr__(self):
        return str(
            {
                "for": {
                    self.variableNameToken.value: self.startValueNode,
                    "to": self.endValueNode,
                    "by": self.stepValueNode,
                    "do": self.bodyNode
                }
            }
        )

class WhileNode:
    def __init__(self, conditionNode, bodyNode):
        self.conditionNode = conditionNode
        self.bodyNode      = bodyNode

    def __repr__(self):
        return str(
            {
                "while": {
                    "condition": self.conditionNode,
                    "do": self.bodyNode
                }
            }
        )

class FunctionDefinitionNode:
    def __init__(self, functionNameToken, argNameTokens, bodyNode):
        self.functionNameToken = functionNameToken
        self.argNameTokens     = argNameTokens
        self.bodyNode          = bodyNode

    def __repr__(self):
        return str(
            {
                "function": {
                    "name": self.functionNameToken.value,
                    "arguments": [arg.value for arg in self.argNameTokens],
                    "body": self.bodyNode
                }
            }
        )

class ReturnNode:
    def __init__(self, nodeToReturn):
        self.nodeToReturn = nodeToReturn

    def __repr__(self):
        return str(
            {
                "return": {
                    "value": self.nodeToReturn
                }
            }
        )

class ContinueNode:
    def __init__(self): pass
    def __repr__(self): return str({"proceedTo": "continue"})

class BreakNode:
    def __init__(self): pass
    def __repr__(self): return str({"proceedTo": "break"})

class CallNode:
    def __init__(self, nodeToCall, argNodes):
        self.nodeToCall = nodeToCall
        self.argNodes   = argNodes

    def __repr__(self):
        return str(
            {
                "call": {
                    "parameters": [argNode for argNode in self.argNodes],
                    "on": self.nodeToCall
                }
            }
        )

class ListNode:
    def __init__(self, nodeList):
        self.nodeList = nodeList

    def __repr__(self):

        nodes = {"Statements": []}
        for node in self.nodeList:
            nodes["Statements"].append(node)

        return str(nodes)
