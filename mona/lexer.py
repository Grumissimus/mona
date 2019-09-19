import mona.token as token
import mona.operator as operator
import mona.keyword as keyword

class Lexer():
	def __init__(self, src = ""):
		self.tokens = []
		self.source = src
		self.srclen = len(src)
		self.srcptr = 0
		self.buffer = []
		self.lineNum = 0
		
	def run(self):
		while self.srcptr < self.srclen:
			if( self.curChar() == "\n" ):
				self.lineNum += 1
				self.srcptr += 1
			elif( self.curChar().isnumeric() ):
				self.getNumber()
			elif( self.curChar().isalpha() or self.curChar() == "_"):
				self.getIdenOrKeyword()
			elif( self.curChar() == "\"" ):
				self.getStringLiteral()
			elif( self.curChar() == "\'" ):
				self.getRawStringLiteral()
			elif( not self.curChar().isalpha() and not self.curChar().isspace() ):
				self.getOperator()
			else:
				self.srcptr += 1
	
	def makeToken(self, type, value, line):
		self.tokens.append( token.Token(type, value, line) )
	
	def curChar(self):
		return self.source[self.srcptr] if self.srcptr < self.srclen else '\0'
		
	def getNumber(self):
		while (self.curChar().isnumeric() or self.curChar() in ['x','X','b','B','.','A','a','C','c','D','d','E','e','F','f']):
			self.buffer.append( self.curChar() )
			self.srcptr += 1
			
		number = "".join(self.buffer)
		value = 0
		
		try:
			if number.startswith("0x") or number.startswith("0X"):
				value = int( number, 16 )
			elif number.startswith("0b") or number.startswith("0B"):
				value = int( number, 2 )
			elif number.startswith("0") and not number.startswith("0."):
				value = int( number, 8 )
			elif "." in number:
				value = float( number )
			else:
				value = int( number, 10 )
		except ValueError:
			return False
			
			
		self.makeToken(token.TOKEN_FLOAT if isinstance(value, float) else token.TOKEN_NUMBER, value, self.lineNum)
		self.buffer = []
		return True
		
	def getIdenOrKeyword(self):
		while self.curChar() == "_" or self.curChar().isalnum():
			self.buffer.append( self.curChar() )
			self.srcptr += 1
			
		value = "".join(self.buffer)
		
		if value == "true" or value == "false":
			self.makeToken(token.TOKEN_BOOLEAN, 1 if value == "true" else 0, self.lineNum);
			self.buffer = []
			return True
		
		try:
			self.makeToken(token.TOKEN_KEYWORD, keyword.keywordMap[value], self.lineNum)
			self.buffer = []
			return True
		except KeyError:
			self.makeToken(token.TOKEN_IDENTIFIER, value, self.lineNum)
			self.buffer = []
			return True
		
	def getStringLiteral(self):
		self.srcptr += 1 #Skip first "
		
		while self.curChar() != "\"" and self.curChar() != '\0':
			self.buffer.append( self.curChar() )
			self.srcptr += 1
		
		self.srcptr += 1 #Skip second "
			
		self.makeToken(token.TOKEN_STRING, "".join(self.buffer).encode('utf-8').decode('unicode_escape'), self.lineNum)
		self.buffer = []
		return True
		
	def getRawStringLiteral(self):
		self.srcptr += 1 #Skip first '
		
		while self.curChar() != "\'" and self.curChar() != '\0':
			self.buffer.append( self.curChar() )
			self.srcptr += 1
		
		self.srcptr += 1 #Skip second '
			
		self.makeToken(token.TOKEN_STRING, "".join(self.buffer), self.lineNum)
		self.buffer = []
		return True
		
	def getOperator(self):
		return False