import mona.token as token
import mona.operator as operator

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
			if(self.curChar() == "\n"):
				self.lineNum += 1
				self.srcptr += 1
			elif( self.curChar().isnumeric() ):
				self.getNumber()
			elif( self.curChar().isalpha() ):
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
			
		self.makeToken(token.TOKEN_NUMBER, int( "".join(self.buffer), 10 ), self.lineNum)
		self.buffer = []
		return True
		
	def getIdenOrKeyword(self):
		return True
		
	def getStringLiteral(self):
		return True
		
	def getRawStringLiteral(self):
		return True
		
	def getOperator(self):
		while not self.curChar().isalnum() and not self.curChar().isspace():
			self.buffer.append( self.curChar() )
			self.srcptr += 1
			
		value = 0
		
		while( self.buffer != [] and not ("".join(self.buffer) in operator.operatorMap.keys()) ):
			self.buffer[:-1]
		
		try:
			value = operator.operatorMap["".join(self.buffer)]
			self.makeToken(token.TOKEN_NONALPHA, value, self.lineNum)	
			self.buffer = []
			return True
		except KeyError:
			return False