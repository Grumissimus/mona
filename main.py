import mona.lexer as lexer
import mona.parser as parser
'''
def main():
	lex = lexer.Lexer("@+$*(?6+1) 2+2")
	lex.run()
	pars = parser.Parser(lex.tokens)
	pars.run()
	return 0

if __name__ == "__main__":
	main()
'''

lex = lexer.Lexer(" return 5 ")
lex.run()
pars = parser.Parser(lex.tokens)
parsingResult = pars.run()
