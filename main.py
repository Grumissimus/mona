from mona.lexer.lexer import Lexer
lex = Lexer("let a := 5\n a := 6 ;will cause error!")
a = lex.run()

for i in lex.tokens:
    print(i)
