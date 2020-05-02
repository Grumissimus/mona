import mona.lexer as lexer
import mona.parser as parser

lex = lexer.Lexer("5")
a = lex.run()
# pars = parser.Parser(lex.tokens)
# parsingResult = pars.run()
