"""
Visitor per interpretar el codi Forth
"""

from forthVisitor import forthVisitor
from forthParser import forthParser
from antlr4 import TerminalNode
from stack import Stack


class MyForthVisitor(forthVisitor):
    """
    Visitor que implementa la semàntica de Forth
    """
    
    def __init__(self):
        """Inicialitza el visitor amb la pila i funcions"""
        self.stack = Stack()
        self.functions = {}
        self.defining = False
        self.current_def = None
        self.def_body = []
        self.current_word = None
    
    def visitProgram(self, ctx):
        """Visita el programa complet"""
        children = ctx.children
        i = 0
        while i < len(children):
            child = children[i]
            if isinstance(child, TerminalNode):
                token = child.symbol
                if token.type == forthParser.COLON:
                    i = self.handle_function_definition(children, i)
                elif token.type == forthParser.SEMICOLON:
                    if self.defining:
                        self.functions[self.current_def] = self.def_body
                        self.defining = False
                        self.current_def = None
                        self.def_body = []
                    else:
                        raise ValueError("Unexpected ;")
                elif self.defining:
                    self.def_body.append(token)
                else:
                    self.handle_token(token)
            i += 1
        return self.stack

    def handle_function_definition(self, children, i):
        """Maneja la definició de funció : word ... ; , retorna el nou index"""
        self.defining = True
        i += 1
        if i < len(children) and isinstance(children[i], TerminalNode) and children[i].symbol.type == forthParser.WORD:
            self.current_def = children[i].symbol.text
            self.def_body = []
        else:
            raise ValueError("Expected word after :")
        return i
    
    def handle_token(self, token):
        """Maneja un token durant l'execució"""
        if token.type == forthParser.NUMBER:
            value = int(token.text)
            self.stack.push(value)
        elif token.type == forthParser.PLUS:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a + b)
        elif token.type == forthParser.MINUS:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a - b)
        elif token.type == forthParser.MULT:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a * b)
        elif token.type == forthParser.DIV:
            b = self.stack.pop()
            a = self.stack.pop()
            try:
                self.stack.push(a // b)
            except ZeroDivisionError:
                raise ValueError("division by zero")
        elif token.type == forthParser.MOD:
            b = self.stack.pop()
            a = self.stack.pop()
            try:
                self.stack.push(a % b)
            except ZeroDivisionError:
                raise ValueError("integer division or modulo by zero")
        elif token.type == forthParser.DOTS:
            print(self.stack.show())
        elif token.type == forthParser.DOT:
            value = self.stack.pop()
            print(value)
        elif token.type == forthParser.SWAP:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(b)
            self.stack.push(a)
        elif token.type == forthParser.TWOSWAP:
            d = self.stack.pop()
            c = self.stack.pop()
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(c)
            self.stack.push(d)
            self.stack.push(a)
            self.stack.push(b)
        elif token.type == forthParser.DUP:
            a = self.stack.peek()
            self.stack.push(a)
        elif token.type == forthParser.TWODUP:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a)
            self.stack.push(b)
            self.stack.push(a)
            self.stack.push(b)
        elif token.type == forthParser.OVER:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a)
            self.stack.push(b)
            self.stack.push(a)
        elif token.type == forthParser.TWOOVER:
            d = self.stack.pop()
            c = self.stack.pop()
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a)
            self.stack.push(b)
            self.stack.push(c)
            self.stack.push(d)
            self.stack.push(a)
            self.stack.push(b)
        elif token.type == forthParser.ROT:
            c = self.stack.pop()
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(b)
            self.stack.push(c)
            self.stack.push(a)
        elif token.type == forthParser.DROP:
            self.stack.pop()
        elif token.type == forthParser.TWODROP:
            self.stack.pop()
            self.stack.pop()
        elif token.type == forthParser.LT:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(-1 if a < b else 0)
        elif token.type == forthParser.GT:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(-1 if a > b else 0)
        elif token.type == forthParser.EQ:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(-1 if a == b else 0)
        elif token.type == forthParser.NE:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(-1 if a != b else 0)
        elif token.type == forthParser.AND:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a & b)
        elif token.type == forthParser.OR:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.push(a | b)
        elif token.type == forthParser.NOT:
            a = self.stack.pop()
            self.stack.push(~a)
        elif token.type == forthParser.WORD:
            word = token.text
            if word in self.functions:
                self.current_word = word
                self.execute_body(self.functions[word])
                self.current_word = None
            else:
                raise ValueError(f"Undefined word: {word}")
    
    def execute_body(self, tokens):
        """Executa una llista de tokens amb suport per condicionals"""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.type == forthParser.IF:
                i = self.handle_conditional(tokens, i)
            elif token.type == forthParser.RECURSE:
                self.execute_body(self.functions[self.current_word])
            elif token.type in (forthParser.ELSE, forthParser.ENDIF):
                # Ja gestionat a l'if
                pass
            else:
                self.handle_token(token)
            i += 1

    def handle_conditional(self, tokens, i):
        """Maneja un bloc conditional if/else/endif, retorna el nou index"""
        # Avalua condició
        cond = self.stack.pop()
        i += 1
        # Troba el bloc if
        start = i
        depth = 0
        while i < len(tokens):
            if tokens[i].type == forthParser.IF:
                depth += 1
            elif tokens[i].type == forthParser.ENDIF:
                if depth == 0:
                    break
                depth -= 1
            elif tokens[i].type == forthParser.ELSE and depth == 0:
                break
            i += 1
        if cond != 0:
            # Executa el bloc if
            self.execute_body(tokens[start:i])
        else:
            # Salta al else o endif
            if i < len(tokens) and tokens[i].type == forthParser.ELSE:
                i += 1
                start = i
                depth = 0
                while i < len(tokens):
                    if tokens[i].type == forthParser.IF:
                        depth += 1
                    elif tokens[i].type == forthParser.ENDIF:
                        if depth == 0:
                            break
                        depth -= 1
                    i += 1
                # Executa el bloc else
                block = tokens[start:i]
                self.execute_body(block)
        # Salta a després del endif
        while i < len(tokens) and tokens[i].type != forthParser.ENDIF:
            i += 1
        return i
