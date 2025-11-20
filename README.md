# Intèrpret de Mini Forth

## Descripció

Intèrpret d'una versió simplificada de Forth implementat amb ANTLR i Python.

## Autors

- [El teu nom]

## Compilació i execució

### Generar els fitxers ANTLR

```bash
make antlr
```

### Executar l'intèrpret interactivament

```bash
python3 -i forth.py
>>> interpret('1 2 + .')
3
>>> quit()
```

### Executar els tests

```bash
make test
```

## Funcionalitats implementades

- [ ] Pila d'avaluació
- [ ] Operacions aritmètiques (+, -, *, /, mod)
- [ ] Manipulació de la pila (swap, dup, over, rot, drop, etc.)
- [ ] Operadors relacionals i booleans
- [ ] Definició i crida de funcions
- [ ] Condicionals (if-else-endif)
- [ ] Recursivitat (recurse)
- [ ] Gestió d'errors (divisió per zero, pila buida)

## Decisions de disseny

### Gramàtica

[Descriure decisions sobre la gramàtica ANTLR]

### Estructura del codi

[Descriure l'organització dels visitadors i classes auxiliars]

### Gestió d'errors

[Descriure com es gestionen els errors d'execució]

## Limitacions conegudes

[Deixar constància de limitacions o parts no implementades]

## Exemples d'ús

```forth
: doble 2 * ;
3 doble .
👉 6

: factorial dup 2 < if drop 1 else dup 1 - faux endif ;
4 factorial .
👉 24
```
