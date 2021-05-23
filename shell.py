from _token      import Token
from lexer       import Lexer
from nodes       import *
from _parser     import *
from context     import *
from classes     import *
from interpreter import *
from hawelTokens import *
from tree        import tree

def block():

    code   = ""
    lineno = 1
    while (line := input(f" {str(lineno).zfill(3)} | ")) != "\\":
        code   += line + '\n'
        lineno += 1

    return code

def shell():

    context_main = Context('main')

    context_main.symbolTable.symbols = \
    {
        'null' : Int(0),
        'true' : Int(1),
        'false': Int(0),
        'pi'   : Int(3.14159265368979),
        'echo' : BuiltInPrint(),
        'get'  : BuiltInInput(),
        'int'  : BuiltInInt(),
        'str'  : BuiltInString(),
        'cls'  : BuiltInClear(),
    }

    showTree   = True
    showTokens = False
    showResult = True

    while True:
        try:
            code = input(" Hwl | ")

            if code == "\\"    : code = block()
            if code == "\\quit": break

            if code == "\\tokens":
                showTokens = not showTokens
                continue

            if code == "\\tree":
                showTree = not showTree
                continue

            if code == "\\result":
                showResult = not showResult
                continue

            tokens = Lexer(TOKENS).lex(code)
            if showTokens:
                for token in tokens: print(token)

            ast    = Parser(tokens).parse()
            if showTree:
                tree(ast)

            result = Interpreter(ast).interpretate(context_main)
            if showResult:
                print(''.join([n.__repr__() for n in result.value.elements]))
            
        except HParsingError as e: e.showError("Hwl", code)
        except HRuntimeError as e: e.showError("Hwl", code)

if __name__ == '__main__' : shell()