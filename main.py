import mona.lexer as lexer
import mona.parser as parser

def main():
	lex = lexer.Lexer("2<<-1")
	lex.run()
	for i in lex.tokens:
		print(i)
	return 0

if __name__ == "__main__":
	main()
