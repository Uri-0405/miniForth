#!/usr/bin/env python3

import sys
from io import StringIO
from contextlib import redirect_stdout
from forth import interpret

def run_test(name, code, expected_output):
    """Executa un test i compara la sortida"""
    f = StringIO()
    try:
        with redirect_stdout(f):
            interpret(code)
        output = f.getvalue().strip()
        if output == expected_output.strip():
            print(f"✓ {name}: PASS")
            return True
        else:
            print(f"✗ {name}: FAIL")
            print(f"  Expected: '{expected_output}'")
            print(f"  Got:      '{output}'")
            return False
    except Exception as e:
        print(f"✗ {name}: ERROR - {e}")
        return False

def main():
    tests = [
        # Pila bàsica
        ("Pila buida .s", ".s", "[]"),
        ("Push números", "1 2 3 .s", "[1, 2, 3]"),
        ("Push zero", "0 .s", "[0]"),
        ("Push negatiu", "-5 .s", "[-5]"),
        ("Push gran", "1000 .s", "[1000]"),
        ("Pop i mostra", "1 2 3 .", "3"),
        ("Múltiples pops", "1 2 3 . . . .s", "3\n2\n1\n[]"),
        ("Error pila buida", "1 . .", "1\nError: Stack is empty"),
        (".s en pila buida", ".s", "[]"),
        
        # Aritmètica
        ("Suma", "1 2 + .", "3"),
        ("Suma zero", "0 0 + .", "0"),
        ("Suma negatius", "-1 -2 + .", "-3"),
        ("Resta", "5 2 - .", "3"),
        ("Resta negatiu", "2 5 - .", "-3"),
        ("Multiplicació", "3 4 * .", "12"),
        ("Multiplicació per zero", "5 0 * .", "0"),
        ("Multiplicació negatius", "-3 -4 * .", "12"),
        ("Divisió", "8 2 / .", "4"),
        ("Divisió per 1", "8 1 / .", "8"),
        ("Divisió amb negatius", "-8 2 / .", "-4"),
        ("Divisió negatiu per negatiu", "-8 -2 / .", "4"),
        ("Mòdul", "7 2 mod .", "1"),
        ("Mòdul zero", "0 5 mod .", "0"),
        ("Mòdul negatiu", "-7 3 mod .", "2"),
        ("Mòdul negatiu divisor", "7 -3 mod .", "-2"),
        
        # Manipulació de pila
        ("Swap", "1 2 3 .s swap .s", "[1, 2, 3]\n[1, 3, 2]"),
        ("Swap amb dos", "1 2 swap .s", "[2, 1]"),
        ("2swap", "1 2 3 4 .s 2swap .s", "[1, 2, 3, 4]\n[3, 4, 1, 2]"),
        ("Dup", "1 2 .s dup .s", "[1, 2]\n[1, 2, 2]"),
        ("Dup zero", "0 dup .s", "[0, 0]"),
        ("2dup", "1 2 3 .s 2dup .s", "[1, 2, 3]\n[1, 2, 3, 2, 3]"),
        ("Over", "1 2 .s over .s", "[1, 2]\n[1, 2, 1]"),
        ("Over amb tres", "1 2 3 over .s", "[1, 2, 3, 2]"),
        ("2over", "1 2 3 4 .s 2over .s", "[1, 2, 3, 4]\n[1, 2, 3, 4, 1, 2]"),
        ("Rot", "1 2 3 .s rot .s", "[1, 2, 3]\n[2, 3, 1]"),
        ("Rot amb quatre", "1 2 3 4 rot .s", "[1, 3, 4, 2]"),
        ("Drop", "1 2 .s drop .s", "[1, 2]\n[1]"),
        ("Drop únic", "1 drop .s", "[]"),
        ("2drop", "1 2 3 .s 2drop .s", "[1, 2, 3]\n[1]"),
        ("2drop tot", "1 2 2drop .s", "[]"),
        
        # Relacionals
        ("Menor que cert", "2 3 < .", "-1"),
        ("Menor que fals", "3 2 < .", "0"),
        ("Menor que igual", "2 2 < .", "0"),
        ("Menor que negatius", "-1 0 < .", "-1"),
        ("Major que cert", "3 2 > .", "-1"),
        ("Major que fals", "2 3 > .", "0"),
        ("Major que igual", "2 2 > .", "0"),
        ("Major que negatius", "0 -1 > .", "-1"),
        ("Igual cert", "2 2 = .", "-1"),
        ("Igual fals", "2 3 = .", "0"),
        ("Igual zero", "0 0 = .", "-1"),
        ("Igual negatius", "-1 -1 = .", "-1"),
        ("Diferent cert", "2 3 <> .", "-1"),
        ("Diferent fals", "2 2 <> .", "0"),
        ("Diferent zero", "0 1 <> .", "-1"),
        
        # Booleans
        ("And cert", "-1 -1 and .", "-1"),
        ("And fals", "-1 0 and .", "0"),
        ("And amb zero", "0 0 and .", "0"),
        ("And amb positiu", "1 -1 and .", "1"),
        ("Or cert", "-1 0 or .", "-1"),
        ("Or fals", "0 0 or .", "0"),
        ("Or amb cert", "-1 -1 or .", "-1"),
        ("Or amb positiu", "1 0 or .", "1"),
        ("Not cert", "0 not .", "-1"),
        ("Not fals", "-1 not .", "0"),
        ("Not positiu", "1 not .", "-2"),
        
        # Funcions
        ("Funció simple", ": doble 2 * ; 4 doble .", "8"),
        ("Funció amb paràmetres", ": suma + ; 3 4 suma .", "7"),
        ("Funció amb crida", ": doble 2 * ; : f doble 1 + ; 3 f .", "7"),
        ("Funció amb condicional", ": abs dup 0 < if 0 swap - endif ; -5 abs .", "5"),
        ("Funció min", ": min 2dup < if drop else swap drop endif ; 3 2 min .", "2"),
        ("Funció max", ": max 2dup > if drop else swap drop endif ; 3 2 max .", "3"),
        ("Funció signe", ": signe dup 0 < if drop -1 else 0 > if 1 else 0 endif endif ; -2 signe .s", "[-1]"),
        ("Funció signe zero", ": signe dup 0 < if drop -1 else 0 > if 1 else 0 endif endif ; 0 signe .s", "[0]"),
        ("Funció signe positiu", ": signe dup 0 < if drop -1 else 0 > if 1 else 0 endif endif ; 5 signe .s", "[1]"),
        ("Funció quadrat", ": quadrat dup * ; 5 quadrat .", "25"),
        ("Funció amb múltiples crides", ": inc 1 + ; : doble inc inc ; 3 doble .", "5"),
        
        # Recursivitat
        ("Factorial 4", ": faux dup rot * swap 1 - dup 2 < if drop else recurse endif ; : factorial dup 2 < if drop 1 else dup 1 - faux endif ; 4 factorial .", "24"),
        ("Factorial 0", ": faux dup rot * swap 1 - dup 2 < if drop else recurse endif ; : factorial dup 2 < if drop 1 else dup 1 - faux endif ; 0 factorial .", "1"),
        ("Factorial 1", ": faux dup rot * swap 1 - dup 2 < if drop else recurse endif ; : factorial dup 2 < if drop 1 else dup 1 - faux endif ; 1 factorial .", "1"),
        ("Factorial 2", ": faux dup rot * swap 1 - dup 2 < if drop else recurse endif ; : factorial dup 2 < if drop 1 else dup 1 - faux endif ; 2 factorial .", "2"),
        ("Factorial 3", ": faux dup rot * swap 1 - dup 2 < if drop else recurse endif ; : factorial dup 2 < if drop 1 else dup 1 - faux endif ; 3 factorial .", "6"),
        ("Fibonacci", ": fib dup 2 < if else dup 1 - recurse swap 2 - recurse + endif ; 6 fib .", "8"),
        
        # Condicionals
        ("If sense else", ": test dup 0 > if 100 . endif ; 5 test", "100"),
        ("If sense else fals", ": test dup 0 > if 100 . endif ; -1 test", ""),
        ("If amb else", ": test dup 0 > if 100 . else 200 . endif ; -1 test", "200"),
        ("If amb else cert", ": test dup 0 > if 100 . else 200 . endif ; 5 test", "100"),
        ("If imbricat", ": test dup 0 > if dup 10 > if 999 . else 888 . endif else 777 . endif ; 15 test", "999"),
        ("If imbricat mig", ": test dup 0 > if dup 10 > if 999 . else 888 . endif else 777 . endif ; 5 test", "888"),
        ("If imbricat fals", ": test dup 0 > if dup 10 > if 999 . else 888 . endif else 777 . endif ; -1 test", "777"),
        ("If amb operacions", ": test dup 0 > if 2 * else + 1 endif ; 3 4 test .", "8"),
        
        # Errors
        ("Divisió per zero", "5 0 / .", "Error: division by zero"),
        ("Mod per zero", "5 0 mod .", "Error: integer division or modulo by zero"),
        ("Pop en pila buida", ".s drop .s", "[]\nError: Stack is empty"),
        ("Swap en pila buida", "swap .s", "Error: Stack is empty"),
        ("Dup en pila buida", "dup .s", "Error: Stack is empty"),
        ("Over en pila buida", "over .s", "Error: Stack is empty"),
        ("Rot en pila buida", "rot .s", "Error: Stack is empty"),
        ("Drop en pila buida", "drop .s", "Error: Stack is empty"),
        ("Paraula indefinida", "undefined .s", "Error: Undefined word: undefined"),
        ("Comentari", "1 2 + . \\ comentari", "3"),
    ]

    passed = 0
    total = len(tests)

    for name, code, expected in tests:
        if run_test(name, code, expected):
            passed += 1

    print(f"\nResultats: {passed}/{total} tests passats")
    if passed == total:
        print("All tests OK")
    else:
        print(f"{total - passed} tests han fallat.")

if __name__ == "__main__":
    main()