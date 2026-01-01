# Makefile per a l'intèrpret de Forth

# Variables
ANTLR = java -jar antlr-4.13.1-complete.jar
PYTHON = python3
GRAMMAR = forth.g4
TEST_FILE = test.txt

# Fitxers generats per ANTLR
GENERATED = forthLexer.py forthParser.py forthVisitor.py forthLexer.tokens forthParser.tokens forth.tokens forth.interp forthLexer.interp

.PHONY: all antlr test clean

# Target per defecte: genera fitxers i executa tests
all: test

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
