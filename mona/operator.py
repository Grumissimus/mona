from enum import Enum

OperatorNames = [
    'TILDE',
    'PLUS',
    'INC',
    'MINUS',
    'DEC',
    'STAR',
    'POWER',
    'DIV',
    'BAND',
    'LAND',
    'BOR',
    'LOR',
    'XOR',
    'MOD',
    'DOLLAR',
    'AT',
    'NOT',
    'GRE',
    'GREQ',
    'LE',
    'LEQ',
    'EQ',
    'QUES',
    'COLON',
    'ASSIGN',
    'DOT',
    'QUOTE',
    'DQUOTE',
    'SQUOTE',
    'SHR',
    'SHL',
    'RANGE',
    'TYPECOL',
    'ISTYPE',
    'SCOLON',
    'POP',
    'PCLS',
    'SOP',
    'SCLS',
    'CBOP',
    'CBCLS',
    'FNARR',
    'COMMA',
    'CUSTOM_OP',
    'TYPEOF',
    'LOOP',
]

Operator = Enum('Operator', " ".join(OperatorNames) )

operatorMap = {
    "~" : Operator.TILDE,
    "+" : Operator.PLUS,
    "++" : Operator.INC,
    "-" : Operator.MINUS,
    "--" : Operator.DEC,
    "*" : Operator.STAR,
    "**" : Operator.POWER,
    "/" : Operator.DIV,
    "&" : Operator.BAND,
    "&&" : Operator.LAND,
    "|" : Operator.BOR,
    "||" : Operator.LOR,
    "^" : Operator.XOR,
    "%" : Operator.MOD,
    "$" : Operator.DOLLAR,
    "@" : Operator.AT,
    "!" : Operator.NOT,
    ">" : Operator.GRE,
    ">=" : Operator.GREQ,
    "<" : Operator.LE,
    "<=" : Operator.LEQ,
    "=" : Operator.EQ,
    "?" : Operator.QUES,
    ":" : Operator.COLON,
    ":=" : Operator.ASSIGN,
    "." : Operator.DOT,
    "\'" : Operator.QUOTE,
    "\"" : Operator.DQUOTE,
    "`" : Operator.SQUOTE,
    ">>" : Operator.SHR,
    "<<" : Operator.SHL,
    ".." : Operator.RANGE,
    "::" : Operator.TYPECOL,
    "?:" : Operator.TYPEOF,
    "::=" : Operator.ISTYPE,
    ";" : Operator.SCOLON,
    "(" : Operator.POP,
    ")" : Operator.PCLS,
    "[" : Operator.SOP,
    "]" : Operator.SCLS,
    "{" : Operator.CBOP,
    "}" : Operator.CBCLS,
    "=>" : Operator.FNARR,
    "," : Operator.COMMA,
    "?*" : Operator.LOOP
}
