grammar StreamerFormula;

formula
    : expr
    ;

expr
    : '(' expr ')'                                                   # parenthesis
    | left=expr '*' right=expr                                       # multiply
    | left=expr '/' right=expr                                       # divide
    | left=expr '+' right=expr                                       # add
    | left=expr '-' right=expr                                       # subtract
    | left=expr '=' right=expr                                       # equal
    | left=expr '>' right=expr                                       # greaterThan
    | left=expr '>=' right=expr                                      # greaterEqual
    | left=expr '<' right=expr                                       # lessThan
    | left=expr '<=' right=expr                                      # lessEqual
    | left=expr '!=' right=expr                                      # notEqual
    | expr 'IN' '(' (expr (',' expr)*)? ')'                          # in
    | expr 'NOT IN' '(' (expr (',' expr)*)? ')'                      # notIn
    | left=expr ('AND'|'&&') right=expr                              # and
    | left=expr ('OR'|'||') right=expr                               # or
    | function                                                       # func
    | 'IF'   expr
      'THEN' expr
      'ELSE' expr
      'ENDIF'                                                        # if
    | 'IF'      expr
      'THEN'    expr
      ('ELSEIF' expr 'THEN' expr)+
      'ELSE' expr
      'ENDIF'                                                        # elseIf
    | Integer                                                        # integer
    | '-'Integer                                                     # integer
    | Decimal                                                        # decimal
    | '-'Decimal                                                     # decimal
    | Datetime                                                       # datetimeLiteral
    | Date                                                           # dateLiteral
    | Field                                                          # field
    | string                                                         # stringLiteral
    ;

function
    : 'POW(' expr ',' expr ')'    # pow
    | 'Min(' expr (',' expr)+ ')' # min
    | 'Max(' expr (',' expr)+ ')' # max
    ;

string
    : SingleQuoteString
    | DoubleQuoteString
    ;

Integer          : [0-9]+ ;
Decimal          : [0-9]*'.'[0-9]+ ;
Date             : ['][0-9][0-9][0-9][0-9]'-'[0-9][0-9]'-'[0-9][0-9] [']
                 | '"'[0-9][0-9][0-9][0-9]'-'[0-9][0-9]'-'[0-9][0-9]'"';
Datetime         : ['][0-9][0-9][0-9][0-9]'-'[0-9][0-9]'-'[0-9][0-9]' '[0-9][0-9]':'[0-9][0-9]':'[0-9][0-9][']
                 | '"'[0-9][0-9][0-9][0-9]'-'[0-9][0-9]'-'[0-9][0-9]' '[0-9][0-9]':'[0-9][0-9]':'[0-9][0-9]'"';
Field            : '[' ~(']')+ ']' ;
SingleQuoteString: ['] ~(['])* ['] ;
DoubleQuoteString: '"' ~('"')* '"' ;
Whitespace       : [ \t\r\n]+ -> skip ;