"""
Implementació de la pila d'avaluació de Forth
"""


class Stack:
    """
    Pila d'avaluació per a l'intèrpret de Forth
    """
    
    def __init__(self):
        """Inicialitza una pila buida"""
        self.stack = []
    
    def push(self, value):
        """Afegeix un valor al cim de la pila"""
        self.stack.append(value)
    
    def pop(self):
        """Treu i retorna el valor del cim de la pila"""
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("Stack is empty")
    
    def is_empty(self):
        """Retorna True si la pila està buida"""
        return len(self.stack) == 0
    
    def peek(self):
        """Retorna el valor del cim sense treure'l"""
        if not self.is_empty():
            return self.stack[-1]
        else:
            raise IndexError("Stack is empty")
    
    def show(self):
        """Retorna una representació de la pila per .s"""
        return str(self.stack)
