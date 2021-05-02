from classes import *
from context import *

class RuntimeResult:
    def __init__(self) : self.reset()

    def reset(self):
        self.value = None
        self.error = None

        self.returnValue    = None
        self.shouldBreak    = False
        self.shouldContinue = False

    def register(self, response):
        if response.error          : self.error          = response.error
        if response.value          : self.value          = response.value
        if response.returnValue    : self.returnValue    = response.returnValue
        if response.shouldBreak    : self.shouldBreak    = response.shouldBreak
        if response.shouldContinue : self.shouldContinue = response.shouldContinue

        return self.value

    def proceed(self, value):
        self.value = value
        return self

    def proceedWithReturn(self, value):
        self.reset()
        self.returnValue = value
        self.value       = value
        return self

    def proceedWithContinue(self):
        self.reset()
        self.shouldContinue = True
        return self

    def proceedWithBreak(self):
        self.reset()
        self.shouldBreak = True
        return self

    def shouldReturn(self):
        return (
            self.error       or 
            self.returnValue or
            self.shouldBreak or 
            self.shouldContinue
        )

    def __repr__(self):
        return f'RTR::({self.value})'

class Interpreter:
    def __init__(self, rootNode):
        self.rootNode = rootNode

    def interpretate(self, context):
        return self.visit(self.rootNode, context)

    def visit(self, node, context):
        return getattr(self, f'visit{type(node).__name__}', self.NoVisitMethodNameDeclared)(node, context)

    def NoVisitMethodNameDeclared(self, node, context):
        raise Exception(f'No visit method for {type(node).__name__} declared')

    def visitIntNode(self, node, context):
        return RuntimeResult().proceed(
            Int(node.token.value)
        )

    def visitStringNode(self, node, context):
        return RuntimeResult().proceed(
            String(node.token.value)
        )

    def visitListNode(self, node, context):
        response = RuntimeResult()
        
        visitedNodes = []
        for elementNode in node.nodeList:
            
            visitedNode = response.register(self.visit(elementNode, context))
            if response.shouldReturn(): return response

            visitedNodes.append(visitedNode)

        return response.proceed(
            List(visitedNodes)
        )

    def visitVariableAccessNode(self, node, context):
        value = context.symbolTable.get(node.variable.value)

        if not value:
            raise SyntaxError(f'Variable "{node.variable.value}" not declared.')

        return RuntimeResult().proceed(value)

    def visitGetNode(self, node, context):
        response = RuntimeResult()

        sliceNode = response.register(self.visit(node.node, context))
        if response.shouldReturn(): return response
        
        from_ = response.register(self.visit(node.slicesNodes[0], context))
        if response.shouldReturn(): return response

        end = response.register(self.visit(node.slicesNodes[1], context))
        if response.shouldReturn(): return response

        return response.proceed(
            sliceNode.getBy(from_, end)
        )

    def visitSetNode(self, node, context):
        response = RuntimeResult()

        nodeToSet = response.register(self.visit(node.node, context))
        if response.shouldReturn(): return response

        index = response.register(self.visit(node.indexNode, context))
        if response.shouldReturn(): return response

        value = response.register(self.visit(node.valueNode, context))
        if response.shouldReturn(): return response

        return response.proceed(
            nodeToSet.setItem(index, value)
        )

    def visitUnaryOpNode(self, node, context):
        response = RuntimeResult()

        value = response.register(self.visit(node.node, context))
        if response.shouldReturn(): return response

        if node.operator.type == 'SUB':
            return response.proceed(value.MUL(Int(-1)))

        if node.operator.type == 'NOT':
            return response.proceed(value.NOT())

        if node.operator.type == 'LENGTH':
            return response.proceed(value.length())

        if node.operator.type == 'HEAD':
            return response.proceed(value.head())

        if node.operator.type == 'TAIL':
            return response.proceed(value.tail())

        return response.proceed(value)

    def visitVariableNode(self, node, context):
        response = RuntimeResult()

        value = response.register(self.visit(node.valueNode, context))
        if response.shouldReturn(): return response

        context.symbolTable.set(node.name, value)

        return response.proceed(value)
        
    def visitBinOpNode(self, node, context):
        response = RuntimeResult()

        left  = response.register(self.visit(node.leftNode, context))
        if response.shouldReturn(): return response
        
        right = response.register(self.visit(node.rightNode, context))
        if response.shouldReturn(): return response

        return response.proceed(getattr(left, node.operation.type)(right))

    def visitIfNode(self, node, context):
        response = RuntimeResult()

        for condition, expression in node.cases:
            conditionValue = response.register(self.visit(condition, context))
            if response.shouldReturn(): return response

            if conditionValue == None: continue # Different types comparissons -> Always False

            if conditionValue.value != 0:
                response.register(self.visit(expression, context))
                if response.shouldReturn(): return response
                
                break

        return response.proceed(Int(0))

    def visitForNode(self, node, context):
        response = RuntimeResult()

        startNode = response.register(self.visit(node.startValueNode, context))
        if response.shouldReturn(): return response

        endNode   = response.register(self.visit(node.endValueNode  , context))
        if response.shouldReturn(): return response

        stepNode  = response.register(self.visit(node.stepValueNode , context))
        if response.shouldReturn(): return response

        for iterator in range(startNode.value, endNode.value, stepNode.value):
            context.symbolTable.set(node.variableNameToken.value, Int(iterator))

            response.register(self.visit(node.bodyNode, context))
            if response.shouldReturn() : return response
            if response.shouldBreak    : break
            if response.shouldContinue : continue

        return response.proceed(Int(0))

    def visitWhileNode(self, node, context):
        response = RuntimeResult()

        while response.register(self.visit(node.conditionNode, context)).value != 0:

            response.register(self.visit(node.bodyNode, context))
            if response.shouldReturn(): return response
            if response.shouldBreak   : break
            if response.shouldContinue: continue

        return response.proceed(Int(0))

    def visitFunctionDefinitionNode(self, node, context):
        functionName = node.functionNameToken.value
        bodyNode     = node.bodyNode
        
        function = Function(functionName, node.argNameTokens, bodyNode, context)

        if node.functionNameToken:
            context.symbolTable.set(functionName, function)

        return RuntimeResult().proceed(function)

    def visitCallNode(self, node, context):
        response = RuntimeResult()

        valueToCall = response.register(self.visit(node.nodeToCall, context))
        if response.shouldReturn(): return response

        args = [response.register(self.visit(argNode, context)) for argNode in node.argNodes]

        return response.proceed(
            valueToCall.execute(args, context)
        )

    def visitReturnNode(self, node, context):
        response = RuntimeResult()

        value = response.register(self.visit(node.nodeToReturn, context))
        if response.shouldReturn(): return response

        return response.proceedWithReturn(value)

    def visitContinueNode(self, node, context):
        return RuntimeResult().proceedWithContinue()

    def visitBreakNode(self, node, context):
        return RuntimeResult().proceedWithBreak()

class Function:
    def __init__(self, name, argNames, bodyNode, context):
        self.name     = name
        self.argNames = argNames
        self.bodyNode = bodyNode
        self.context  = context

    def execute(self, args, _: "<unused>"):
        if len(args) > len(self.argNames):
            raise SyntaxError(f'Too many arguments given to "{self.name}".')
        if len(args) < len(self.argNames):
            raise SyntaxError(f'Too few arguments given to "{self.name}".')

        self.context = Context(self.name, self.context)

        for i in range(len(args)):
            argName  = self.argNames[i].value
            argValue = args[i]
            self.context.symbolTable.set(argName, argValue)

        response = RuntimeResult()

        value = response.register(Interpreter(self.bodyNode).interpretate(self.context))
        if response.shouldReturn() and response.returnValue == None: return response
        
        return value # if value else Int(0)

    def __repr__(self):
        return f'<function {self.name}>'

class BuiltInPrint:
    
    @staticmethod
    def execute(args, context):
        try:
            if args[0].value == "-n": print(*args[1:], end = ''  )
            else                    : print(*args    , end = "\n")
        except AttributeError       : print(*args    , end = "\n")
        except IndexError           : print()
        
        return Int(0)

    def __repr__(self):
        return f'<{self.__class__}>'

class BuiltInInput:
    
    @staticmethod
    def execute(args, context):
        return String(input(*args))

    def __repr__(self):
        return f'<{self.__class__}>'

class BuiltInInt:
    
    @staticmethod
    def execute(args, context):
        return Int(int(args[0].value))

    def __repr__(self):
        return f'<{self.__class__}>'

class BuiltInString:
    
    @staticmethod
    def execute(args, context):
        return String(str(args[0].value))

    def __repr__(self):
        return f'<{self.__class__}>'