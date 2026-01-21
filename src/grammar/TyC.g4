grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self): 
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options{
	language=Python3;
}

// TODO: Define grammar rules here
program 
    : (structdec | functiondec)* EOF
    ;
//--------------------------------PARSER--------------------
//struct Declare
structdec
    : STRUCT ID LBRACE structmem+ RBRACE SEMI
    ;

//struct members
structmem
    : type ID SEMI
    ;
// function Declare
functiondec
    : (type | VOID)? ID LPAREN (parameterlist)? RPAREN block
    ;
// parameter list
parameterlist
    : parameter (COMMA parameter)*
    ;

// SINGLE parameter
parameter
    : type ID 
    ;

// STATEMENT block
block   
    : LBRACE RBRACE
    ;
//----------------------------LEXER----------------------
//type
type
    : INT
    | FLOAT
    | STRING
    | AUTO
    | ID        
//    | STRUCT ID
    ;
// KEYWORD
INT     : 'int';
FLOAT   : 'float';
STRING  : 'string';
VOID    : 'void';
STRUCT  : 'struct';
AUTO    : 'auto';

// SEPARATOR 
LPAREN  : '(';
RPAREN  : ')';
LBRACE  : '{';
RBRACE  : '}';
COMMA   : ',';
SEMI    : ';';

//IDENTIFIER
ID 
    :[a-zA-Z_] [a-zA-Z_0-9]*
    ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;
ILLEGAL_ESCAPE:.;
UNCLOSE_STRING:.;
