from _token      import Token
from lexer       import Lexer
from nodes       import *
from _parser     import *
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
        'null' : Int(0),
        'true' : Int(1),
        'false': Int(0),
        'pi'   : Int(3.14159265368979),
        'echo' : BuiltInPrint(),
        'get'  : BuiltInInput(),
        'int'  : BuiltInInt(),
        'str'  : BuiltInString(),
    }

    if len(sys.argv) == 1:

        while True:

            code = input("<DEBUG> ")

            tokens = Lexer(TOKENS).lex(code)
            print(f"\nToken List: {tokens}")

            ast = Parser(tokens).parse()
            if ast.error: ReconstructError(code, tokens, ast).reconstruct(); break

            print(f'\nAST:\n{json.dumps(eval(ast.value.__repr__()), indent = 2)}')

            result = Interpreter(ast.value).interpretate(context_main)
            print(f'\nresult: {result}')
        
    else:
        with open(f'{sys.argv[1]}', 'r') as file:
            code   = file.read()

            tokens = Lexer(TOKENS).lex(code)

            ast    = Parser(tokens).parse()

            if ast.error: ReconstructError(code, tokens, ast).reconstruct(); exit(1)

            Interpreter(ast.value).interpretate(context_main)

if __name__ == '__main__': main()
