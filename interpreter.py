from classes import *
from context import *

class HRuntimeError (Exception):

    def __init__(self, message, token, contextName):
        self.message     = message
        self.token       = token
        self.contextName = contextName

    def showError(self, context, code):
        # Just Some Coloring
        Red     = "\x1b[38;2;251;73;52m"
        Purple  = "\x1b[38;2;211;134;155m"
        Cyan    = "\x1b[38;2;142;192;124m"
        Orange  = "\x1b[38;2;254;128;25m"
        Default = "\x1b[0m"

        print(f'\n[{Cyan}{context}{Default}:{Purple}{self.token.line}{Default}:{Purple}{self.token.begin}{Default}] Context: {Cyan}{self.contextName}{Default}: ({Orange}Execution{Default}) {Red}Error{Default}: {self.message}.\n')

        spacing = ' ' * (self.token.begin)
        pointTo = '^' * (self.token.end - self.token.begin + 1) 
        nLength = " " * len(str(self.token.line))

        line = code.split("\n")[self.token.line - 1]
        line = list(line)
        line.insert(self.token.begin  , Orange )
        line.insert(self.token.end + 2, Default)
        line = ''.join(line)

        print(f' {nLength} | ')
        print(f' {Purple}{self.token.line}{Default} | {line}')
        print(f' {nLength} | {Red}{spacing}{pointTo}{Default}\n')

class RuntimeResult:
    def __init__(self) : self.reset()

    def reset(self):
        self.value = None

        self.returnValue    = None
        self.shouldBreak    = False
        self.shouldContinue = False

    def register(self, response):
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
        return self.returnValue or \
               self.shouldBreak or \
               self.shouldContinue

    def properFormat(self):
        return f'{self.value}'[1:-1]

    def __repr__(self):
        return f'RTR::(\n    {self.value}\n)'

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
            raise HRuntimeError(f'Identifier "{node.variable.value}" not declared. (Yet?)', node.variable, context.contextName)

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

    def visitTernaryNode(self, node, context):
        response = RuntimeResult()

        condition = response.register(self.visit(node.condition, context))
        if response.shouldReturn(): return response

        if condition != None:
            if condition.value != 0:
                case = response.register(self.visit(node.caseTrueNode, context))
                if response.shouldReturn(): return response
                
                return response.proceed(case)
        
        case = response.register(self.visit(node.caseFalseNode, context))
        if response.shouldReturn(): return response

        return response.proceed(case)

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
            if response.shouldContinue : response.reset(); continue
            if response.shouldBreak    : response.reset(); break
            if response.shouldReturn() : return response

        return response.proceed(Int(0))

    def visitForEachNode(self, node, context):
        response = RuntimeResult()

        iterable = response.register(self.visit(node.iterableNode, context))
        if response.shouldReturn(): return response

        for iterator in iterable.iter():
            context.symbolTable.set(node.variableNameToken.value, iterator)

            response.register(self.visit(node.bodyNode, context))
            if response.shouldContinue : response.reset(); continue
            if response.shouldBreak    : response.reset(); break
            if response.shouldReturn() : return response

        return response.proceed(Int(0))

    def visitWhileNode(self, node, context):
        response = RuntimeResult()

        while response.register(self.visit(node.conditionNode, context)).value != 0:

            response.register(self.visit(node.bodyNode, context))
            if response.shouldContinue : response.reset(); continue
            if response.shouldBreak    : response.reset(); break
            if response.shouldReturn(): return response

        return response.proceed(Int(0))

    def visitFunctionDefinitionNode(self, node, context):
        functionName = node.functionNameToken
        bodyNode     = node.bodyNode
        
        function = Function(functionName, node.argNameTokens, bodyNode, context)

        if node.functionNameToken:
            context.symbolTable.set(functionName.value, function)

        return RuntimeResult().proceed(function)

    def visitCallNode(self, node, context):
        response = RuntimeResult()

        valueToCall = response.register(self.visit(node.nodeToCall, context))
        if response.shouldReturn(): return response

        args = [response.register(self.visit(argNode, context)) for argNode in node.argNodes]

        return response.proceed(
            valueToCall.execute(args, context, node.nodeToCall)
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

    def execute(self, args, _: "<unused>", where):
        if len(args) > len(self.argNames):
            raise HRuntimeError(f'Too many arguments given to "{self.name.value}"', where.variable, self.context.contextName)
        if len(args) < len(self.argNames):
            raise HRuntimeError(f'Too few arguments given to "{self.name.value}"', where.variable, self.context.contextName)

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
        return f'<function "{self.name.value}">'

class BuiltInPrint:
    
    @staticmethod
    def execute(args, context):
        try:
            if args[0].value == "-n": print(*args[1:] , end = ''  )
            else                    : print(''.join([str(arg) for arg in args]), end = "\n")
        except AttributeError       : print(''.join([str(arg) for arg in args]), end = "\n")
        except IndexError           : print()
        
        return Int(0)

    def __repr__(self):
        return f'{self.__class__}'

class BuiltInInput:
    
    @staticmethod
    def execute(args, context):
        return String(input(*args))

    def __repr__(self):
        return f'{self.__class__}'

class BuiltInInt:
    
    @staticmethod
    def execute(args, context):
        return Int(int(args[0].value))

    def __repr__(self):
        return f'{self.__class__}'

class BuiltInString:
    
    @staticmethod
    def execute(args, context):
        return String(str(args[0].value))

    def __repr__(self):
        return f'{self.__class__}'