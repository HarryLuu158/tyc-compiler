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
//-------------------------------- PARSER --------------------
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
    : LBRACE STATEMENT* RBRACE
    ;

//STATEMENT
STATEMENT
    : block                                             # Block
    | varDeclStmt                                       # VarDec
    | IF LPAREN expr RPAREN stmt (ELSE stmt)?           # If
    | WHILE LPAREN expr RPAREN stmt                     # While
    | FOR LPAREN forInit? SEMI expr? SEMI expr? RPAREN stmt # For
    | SWITCH LPAREN expr RPAREN LBRACE switchCase* RBRACE # Switch
    | BREAK SEMI                                        # Break
    | CONTINUE SEMI                                     # Continue
    | RETURN expr? SEMI                                 # Return
    | expr SEMI                                         # Expr
    | SEMI                                              # Empty
    ;

varDeclStmt
    : varDecl SEMI
    ;

varDecl
    : type ID ASSIGN (expr)?
    | AUTO ID ASSIGN (expr)?
    ;

switchCase
    : (CASE expr COLON | DEFAULT COLON)+ STATEMENT*
    ;

forInit
    : varDecl
    | expr
    ;

//expressions
expr
    : primary                                           # PrimaryExpr
    | expr (INC | DEC)                                  # PostfixExpr
    | (INC | DEC) expr                                  # PrefixExpr
    | (BANG | ADD | SUB) expr                           # UnaryExpr
    | expr DOT ID                                       # MemberAccessExpr
    | expr (MUL | DIV | MOD) expr                       # MultiExpr
    | expr (ADD | SUB) expr                             # AddExpr
    | expr (LT | GT | LE | GE) expr                     # RelationalExpr
    | expr (EQUAL | NOTEQUAL) expr                      # EqualityExpr
    | expr AND expr                                     # LogicAndExpr
    | expr OR expr                                      # LogicOrExpr
    | <assoc=right> expr ASSIGN expr                    # AssignExpr
    ;

primary
    : LPAREN expr RPAREN
    | literal
    | ID LPAREN (expr (COMMA expr)*)? RPAREN  // Function Call
    | ID
    ;

literal
    : INT_LIT | FLOAT_LIT | STRING_LIT
    ;

//types
type
    : INT 
    | FLOAT 
    | STRING 
    | AUTO
    | ID  
    ;

//------------------------------ LEXER ------------------------------

FLOAT_LIT
    : [0-9]+ '.' [0-9]* EXPONENT?
    | '.' [0-9]+ EXPONENT?
    | [0-9]+ EXPONENT
    ;

fragment EXPONENT : [eE] [+-]? [0-9]+ ;

INT_LIT : '0' | [1-9] [0-9]* ;

STRING_LIT : '"' (ESC_SEQ | ~["\\\r\n])* '"' ;

fragment ESC_SEQ : '\\' [bfrn"t\\] ;

// SEPARATOR
LPAREN  : '(';
RPAREN  : ')';
LBRACE  : '{';
RBRACE  : '}';
COMMA   : ',';
SEMI    : ';';

//Operator
ADD     : '+';
SUB     : '-';
MUL     : '*';
DIV     : '/';
MOD     : '%';
EQUAL   : '==';
NOTEQUAL: '!=';
LT      : '<';
GT      : '>';
LE      : '<=';
GE      : '>=';
OR      : '||';
AND     : '&&';
NOT     : '!';
INC     : '++';
DEC     : '--';
ASSIGN  : '=';
MEMACC  : '.';

// Keyword
BREAK   : 'break';
CASE    : 'case';
CONTINUE: 'continue';
DEFAULT : 'default';
ELSE    : 'else';
FOR     : 'for';
IF      : 'if';
RETURN  : 'return';
SWITCH  : 'switch';
WHILE   : 'while';
INT     : 'int';
FLOAT   : 'float';
STRING  : 'string';
VOID    : 'void';
STRUCT  : 'struct';
AUTO    : 'auto';

//Identifier
ID 
    :[a-zA-Z_] [a-zA-Z_0-9]*
    ;

//Comment
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;
LINE_COMMENT  : '//' ~[\r\n]* -> skip ;

//Character Set
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs

ERROR_CHAR: .;
ILLEGAL_ESCAPE:.;
UNCLOSE_STRING:.;
