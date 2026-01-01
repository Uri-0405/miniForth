# Intèrpret de Mini Forth

## Descripció

Aquest projecte implementa un intèrpret complet per al miniForth, utilitzant ANTLR per al parsing i Python per a l'execució. L'objectiu és demostrar el funcionament d'un llenguatge basat en pila amb característiques avançades com funcions i recursivitat.

## Característiques

- **Operacions de pila**: Suport per push, pop, dup, swap, over, rot, drop, etc., amb gestió d'errors per piles buides.
- **Aritmètica**: Operacions bàsiques (+, -, *, /, mod) amb divisió entera, incloent casos amb negatius.
- **Relacionals**: Comparacions (<, >, =, <>) amb valors de veritat típics de Forth (-1 per cert, 0 per fals).
- **Booleans**: Operacions bit a bit (and, or, not).
- **Funcions**: Definició i crida de paraules amb : i ;, permetent reutilitzar codi.
- **Condicionals**: Blocs if/else/endif amb niuament.
- **Recursivitat**: Comanda 'recurse' per funcions recursives.
- **Comentaris**: Suport per comentaris d'estil `( ... )`, útils per documentar el codi.
- **Gestió d'errors**: Detecció d'errors bàsics com divisió per zero, piles buides o paraules indefinides, amb missatges clars.

## Decisions de Disseny

Per complir amb els requisits de robustesa, modularitat i claredat, s'han pres les següents decisions arquitectòniques:

1.  **Separació de la Pila (`Stack`)**:
    - S'ha creat una classe `Stack` independent a `stack.py` per encapsular tota la lògica de manipulació de dades.
    - Això permet centralitzar la gestió d'errors (com `pop` en pila buida) en un sol lloc, llançant excepcions personalitzades que el visitor captura.

2.  **Visitor amb Estat**:
    - La classe `MyForthVisitor` manté l'estat de l'execució (la pila i el diccionari de funcions).
    - Per a la definició de funcions (`: ... ;`), s'ha optat per un mode "gravació" (`self.defining`) que emmagatzema els tokens del cos de la funció en lloc d'executar-los immediatament. Això simplifica el parsing i permet reutilitzar el mateix visitor.

3.  **Gestió de la Recursivitat**:
    - La comanda `recurse` s'implementa buscant la funció actualment en execució dins el diccionari de funcions i tornant a visitar el seu cos.
    - Això evita haver de crear nous objectes visitor per a cada crida recursiva, mantenint l'eficiència i compartint la mateixa pila de dades.

4.  **Gestió d'Errors**:
    - S'utilitza un bloc `try-except` global al punt d'entrada (`forth.py`) per capturar qualsevol excepció (sintàctica o d'execució) i mostrar un missatge d'error net sense aturar l'intèrpret abruptament.

## Requisits previs

- **Python 3.x**: Necessari per executar l'intèrpret.
- **Java (JRE/JDK)**: Necessari per generar el parser amb ANTLR4.

## Instal·lació i configuració

1. **Clonar o descarregar el projecte** i accedir al directori.

2. **Crear un entorn virtual (opcional però recomanat):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # A Linux/Mac
   # .venv\Scripts\activate   # A Windows
   ```

3. **Instal·lar les dependències de Python:**
   ```bash
   pip install antlr4-python3-runtime
   ```

4. **Obtenir l'eina ANTLR4:**
   Descarrega `antlr-4.13.1-complete.jar` de [la web oficial](https://www.antlr.org/download.html) o utilitza la comanda següent si tens `curl`:
   ```bash
   curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar
   ```

5. **Generar el parser:**
   Pots utilitzar el `Makefile` inclòs:
   ```bash
   make antlr
   ```
   O executar la comanda manualment:
   ```bash
   java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -no-listener -visitor forth.g4
   ```

## Ús

### Executar l'intèrpret (Mode interactiu)
```bash
python forth.py
```
Exemple de sessió:
```
forth> 1 2 + .
3
forth> : quadrat dup * ; 5 quadrat .
25
forth> quit
```

### Executar els tests
El projecte inclou un conjunt de proves a `test.txt`. Pots executar-les amb:
```bash
make test
```
O manualment amb:
```bash
python -m doctest test.txt -v
```

## Estructura del projecte

- `forth.g4`: Gramàtica ANTLR que defineix la sintaxi.
- `forth.py`: Punt d'entrada principal i bucle REPL.
- `visitor.py`: Implementació del visitor que executa la lògica del llenguatge.
- `stack.py`: Implementació de la pila de dades.
- `test.txt`: Fitxer de text amb proves `doctest`.
- `Makefile`: Automatització de tasques (generació de parser, tests).
- Fitxers generats (`forthLexer.py`, `forthParser.py`, etc.): Codi generat per ANTLR.

## Dependències

- Python 3.x
- `antlr4-python3-runtime`
- Java (només per a la generació del parser)
