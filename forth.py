"""
Intèrpret de Mini Forth
"""

from antlr4 import *
from forthLexer import forthLexer
from forthParser import forthParser
from visitor import MyForthVisitor


def interpret(code: str) -> None:
    """
    Interpreta i executa codi Forth.
    
    Args:
        code: String amb el codi Forth a executar
    """
    input_stream = InputStream(code)
    lexer = forthLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = forthParser(token_stream)
    tree = parser.program()
    
    visitor = MyForthVisitor()
    try:
        visitor.visit(tree)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    # Mode interactiu
    print("Mini Forth Interpreter")
    print("Escriu codi Forth o 'quit' per sortir")
    from visitor import MyForthVisitor
    visitor = MyForthVisitor()
    while True:
        try:
            code = input("forth> ")
            if code.strip() == 'quit':
                break
            input_stream = InputStream(code)
            lexer = forthLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = forthParser(token_stream)
            tree = parser.program()
            visitor.visit(tree)
        except Exception as e:
            print(f"Error: {e}")
