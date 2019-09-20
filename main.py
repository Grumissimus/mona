import mona.keyword as keyword
import mona.operator as operator
import mona.token as token
import mona.lexer as lexer

def main():
	lex = lexer.Lexer("let a := [ 1 2 3 ]")
	lex.run()
	for i in lex.tokens:
		print(i)
	return 0

if __name__ == "__main__":
	main()