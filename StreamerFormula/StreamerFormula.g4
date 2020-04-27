grammar StreamerFormula;

formula
    : expr
    ;

expr
    : function                                            # func
    | expr '+' expr                                       # add
    | expr '-' expr                                       # subtract
    | expr '*' expr                                       # multiply
    | expr '/' expr                                       # divide
    | expr ('AND'|'&&') expr                              # and
    | expr ('OR'|'||') expr                               # or
    | expr '=' expr                                       # equal
    | expr '>' expr                                       # greaterThan
    | expr '>=' expr                                      # greaterEqual
    | expr '<' expr                                       # lessThan
    | expr '<=' expr                                      # lessEqual
    | expr '!=' expr                                      # notEqual
    | expr 'IN' parens                                    # in
    | expr 'NOT IN' parens                                # notIn
    | 'IF' expr 'THEN' expr 'ELSE' expr 'ENDIF'           # if
    | 'IF' expr 'THEN' expr
      ('ELSEIF' expr 'THEN' expr)+ 'ELSE' expr 'ENDIF'    #elseIf
    | parens                                              # parenthesis
    | number                                              # numberLiteral
    | string                                              # stringLiteral
    | Date                                                # dateLiteral
    | Field                                               # field
    ;

function
    :  'POW(' expr ',' expr ')'    # pow
    |  'Min(' expr (',' expr)+ ')' # min
    |  'Max(' expr (',' expr)+ ')' # max
    ;

parens
    : '(' expr ')'
    ;

number
    : Integer
    | Decimal
    ;

string
    : SingleQuoteString
    | DoubleQuoteString
    ;

Integer          : '-'?[0-9]+ ;
Decimal          : '-'?[0-9]*'.'[0-9]+ ;
Date             : [0-9][0-9][0-9][0-9]'-'[0-9][0-9]'-'[0-9][0-9] ;
Field            : '[' ~(']')+ ']' ;
SingleQuoteString: ['] ~(['])* ['] ;
DoubleQuoteString: '"' ~('"')* '"' ;
Whitespace       : [ \t\r\n]+ -> skip ;