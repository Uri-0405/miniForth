grammar forth;

program
    : (NUMBER | PLUS | MINUS | MULT | DIV | MOD | DOTS | DOT | SWAP | TWOSWAP | DUP | TWODUP | OVER | TWOOVER | ROT | DROP | TWODROP | LT | GT | EQ | NE | AND | OR | NOT | COLON | SEMICOLON | WORD | IF | ELSE | ENDIF | RECURSE)* EOF
    ;

// Lexer rules

COMMENT
    : '\\' ~[\r\n]* -> skip
    ;

NUMBER
    : '-'? [0-9]+
    ;

PLUS
    : '+'
    ;

MINUS
    : '-'
    ;

MULT
    : '*'
    ;

DIV
    : '/'
    ;

MOD
    : 'mod'
    ;

DOTS
    : '.s'
    ;

DOT
    : '.'
    ;

SWAP
    : 'swap'
    ;

TWOSWAP
    : '2swap'
    ;

DUP
    : 'dup'
    ;

TWODUP
    : '2dup'
    ;

OVER
    : 'over'
    ;

TWOOVER
    : '2over'
    ;

ROT
    : 'rot'
    ;

DROP
    : 'drop'
    ;

TWODROP
    : '2drop'
    ;

LT
    : '<'
    ;

GT
    : '>'
    ;

EQ
    : '='
    ;

NE
    : '<>'
    ;

AND
    : 'and'
    ;

OR
    : 'or'
    ;

NOT
    : 'not'
    ;

COLON
    : ':'
    ;

SEMICOLON
    : ';'
    ;

IF
    : 'if'
    ;

ELSE
    : 'else'
    ;

ENDIF
    : 'endif'
    ;

RECURSE
    : 'recurse'
    ;

WORD
    : [a-zA-Z_][a-zA-Z0-9_]*
    ;

WS
    : [ \t\r\n]+ -> skip
    ;
