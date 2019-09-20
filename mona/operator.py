TILDE = 0		#~
PLUS = 1		#+
INC = 2			#++
MINUS = 3		#-
DEC = 4			#--
STAR = 5		#*
POWER = 6		#**
DIV = 7			#/
BAND = 8		#&
LAND = 9		#&&
BOR = 10		#|
LOR = 11		#||
XOR = 12		#^
MOD = 13		#%
DOLLAR = 14		#$
AT = 15			#@
NOT = 16		#!
GRE = 17		#>
GREQ = 18		#>=
LE = 19			#<
LEQ = 20		#<=
EQ = 21			#=
QUES = 22		#?
COLON = 23		#:
ASSIGN = 24 	#:=
DOT = 25		#.
QUOTE = 26		#'
DQUOTE = 27		#"
SQUOTE = 28		#`
SHR = 29		#>>
SHL = 30		#<<
RANGE = 31		#..
TYPECOL = 32	#::
TYPEOF = 33		#?::
SCOLON = 34 	#;
POP = 35		#(
PCLS = 36		#)
SOP	= 37		#[
SCLS = 38		#]
CBOP = 39		#{
CBCLS = 40		#}
FNARR = 41		#=>
COMMA = 42		#,
CUSTOM_OP = 43	#

operatorMap = {
	"~" : TILDE,
	"+" : PLUS,
	"++" : INC,
	"-" : MINUS,
	"--" : DEC,
	"*" : STAR,
	"**" : POWER,
	"/" : DIV,
	"&" : BAND,
	"&&" : LAND,
	"|" : BOR,
	"||" : LOR,
	"^" : XOR,
	"%" : MOD,
	"$" : DOLLAR,
	"@" : AT,
	"!" : NOT,
	">" : GRE,
	">=" : GREQ,
	"<" : LE,
	"<=" : LEQ,
	"=" : EQ,
	"?" : QUES,
	":" : COLON,
	":=" : ASSIGN,
	"." : DOT,
	"\'" : QUOTE,
	"\"" : DQUOTE,
	"`" : SQUOTE,
	">>" : SHR,
	"<<" : SHL,
	".." : RANGE,
	"::" : TYPECOL,
	"?::" : TYPEOF,
	";" : SCOLON,
	"(" : POP,
	")" : PCLS,
	"[" : SOP,
	"]" : SCLS,
	"{" : CBOP,
	"}" : CBCLS,
	"=>": FNARR,
	"," : COMMA
}
