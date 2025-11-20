# Makefile per a l'intèrpret de Forth

# Variables
ANTLR = antlr4
PYTHON = python3
GRAMMAR = forth.g4
TEST_FILE = test.txt

# Fitxers generats per ANTLR
GENERATED = forthLexer.py forthParser.py forthListener.py forthVisitor.py

.PHONY: all antlr test clean

# Target per defecte
all: antlr

# Generar els fitxers Python a partir de la gramàtica ANTLR
antlr: $(GRAMMAR)
	$(ANTLR) -Dlanguage=Python3 -no-listener -visitor $(GRAMMAR)

# Executar els tests amb doctest
test: antlr
	$(PYTHON) -m doctest $(TEST_FILE) -v

# Netejar els fitxers generats
clean:
	rm -f $(GENERATED)
	rm -rf __pycache__
	rm -f *.pyc
	rm -f *.tokens
	rm -f *.interp
