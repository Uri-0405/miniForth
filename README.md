# Intèrpret de Mini Forth 

## Descripció

Aquest projecte implementa un intèrpret complet per al  miniForth, utilitzant ANTLR per al parsing i Python per a l'execució. L'objectiu és demostrar el funcionament d'un llenguatge basat en pila amb característiques avançades com funcions i recursivitat.

## Característiques

- **Operacions de pila**: Suport per push, pop, dup, swap, over, rot, drop, etc., amb gestió d'errors per piles buides.
- **Aritmètica**: Operacions bàsiques (+, -, *, /, mod) amb divisió entera, incloent casos amb negatius.
- **Relacionals**: Comparacions (<, >, =, <>) amb valors de veritat típics de Forth (-1 per cert, 0 per fals).
- **Booleans**: Operacions bit a bit (and, or, not).
- **Funcions**: Definició i crida de paraules amb : i ;, permetent reutilitzar codi.
- **Condicionals**: Blocs if/else/endif amb niuament.
- **Recursivitat**: Comanda 'recurse' per funcions recursives.
- **Comentaris**: Suport per comentaris d'estil ( ), útils per documentar el codi.
- **Gestió d'errors**: Detecció d'errors bàsics com divisió per zero, piles buides o paraules indefinides, amb missatges clars.

## Instal·lació i configuració

1. Instal·lar ANTLR4: Descarregar antlr-4.13.1-complete.jar de https://www.antlr.org/download.html i col·locar-lo al directori del projecte.
2. Generar el parser: Executar `java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -no-listener -visitor forth.g4`.
3. Executar l'intèrpret: `python forth.py`.
4. Executar els tests: `python test.py`.

## Ús

### Mode interactiu
python forth.py
forth> 1 2 + .
3
forth> : quadrat dup * ; 5 quadrat .
25
forth> quit

### Execució de programes
Pots passar codi directament a la funció `interpret(codi)` o introduir-lo en mode interactiu.

## Fitxers

- `forth.g4`: Gramàtica ANTLR que defineix la sintaxi.
- `forth.py`: Punt d'entrada principal, amb mode interactiu que em facilitava les proves ràpides.
- `visitor.py`: Implementa el visitor per executar el codi.
- `stack.py`: Classe per gestionar la pila.
- `test.py`: Suite de tests completa per validar el funcionament.
- Fitxers generats: `forthLexer.py`, `forthParser.py`, `forthVisitor.py`.

## Dependències

- Python 3.x
- ANTLR4 runtime
