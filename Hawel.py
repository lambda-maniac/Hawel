from _token      import Token
from lexer       import Lexer
from nodes       import *
from _parser     import *
from context     import *
from classes     import *
from interpreter import *
from hawelTokens import *
from tree        import tree

def main():

    import sys

    # Setup Context
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

    if len(sys.argv) == 1:

        while True:
            try:
                code = input("(Hwl) ")

                tokens = Lexer(TOKENS).lex(code)

                ast = Parser(tokens).parse()
                tree(ast, indent="")

                result = Interpreter(ast).interpretate(context_main)
                print(f'\nresult: {result}')
                
            except HParsingError as e: e.showError("(Hwl)", code)
            except HRuntimeError as e: e.showError("(Hwl)", code)
        
    else:
        try:
            with open(f'{sys.argv[1]}', 'r') as file:
                Interpreter(Parser(Lexer(TOKENS).lex(file.read())).parse()).interpretate(context_main)
        
        except HParsingError as e:
            with open(f'{sys.argv[1]}', 'r') as file:
                e.showError(file.name, file.read())

        except HRuntimeError as e:
            with open(f'{sys.argv[1]}', 'r') as file:
                e.showError(file.name, file.read())

if __name__ == '__main__': main()
