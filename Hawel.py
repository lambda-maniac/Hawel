from _token      import Token
from lexer       import Lexer
from nodes       import *
from _parser     import Parser
from context     import *
from classes     import *
from interpreter import *
from hawelTokens import *

def main():

    import sys
    import json

    # Setup Context
    context_main = Context('main')

    context_main.symbolTable.symbols = \
    {
        'null': Int(0),
        'pi'  : Int(3.14159265368979),
        'echo': BuiltInPrint(),
        'get' : BuiltInInput(),
        'int' : BuiltInInt(),
        'str' : BuiltInString(),
    }

    if len(sys.argv) == 1:

        while True:

            tokens = Lexer(TOKENS).lex(input("<DEBUG> "))
            print(f"\nToken List: {tokens}")

            ast = Parser(tokens).parse()
            print(f'\nAST:\n{json.dumps(eval(ast.__repr__()), indent = 2)}')

            result = Interpreter(ast).interpretate(context_main)
            print(f'\nresult: {result}')
        
    else:
        with open(f'{sys.argv[1]}', 'r') as file:
            Interpreter(Parser(Lexer(TOKENS).lex(file.read())).parse()).interpretate(context_main)

if __name__ == '__main__': main()
