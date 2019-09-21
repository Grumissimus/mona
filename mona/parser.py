import mona.token as token
import mona.operator as operator
import mona.keyword as keyword
import mona.ast as ast
import mona.types as types
import mona.symbol as symbol

import sys

class Parser():
	def __init__(self, tok):
		self.tokens = token
		self.tokptr = 0
		self.program = []
		self.types = types.constructDefaultGraph()
		self.emf = expr_literal
		
	def run():
		while( self.cur() != None ):
			ast = None
			
			ast = self.emf()
			
			continue
	
	def expr_literal():
		if( self.cur().type in [token.TOKEN_NUMBER, token.TOKEN_FLOAT, token.TOKEN_STRING, token.BOOLEAN] ):
			tok = LiteralAST(self.cur())
			self.next()
			return tok
		elif( self.check(token.TOKEN_IDENTIFIER) ):
			tok = IdenAST(self.cur())
			self.next()
			return tok
		elif( self.check(token.TOKEN_NONALPHA, POP) ):
			self.next()
			tok = self.emf()
			self.expect(token.TOKEN_NONALPHA, PCLS)
			return tok
	
	def croak(self,errorMessage):
		print(errorMessage, file=sys.stderr);
		sys.exit()
	
	def expect(self, type, value = 0, onfail = ""):
		curtok = self.cur()
		if not curtok.type == type if value == 0 else curtok.type == type and curtok.value == value:
			self.croak(onfail)
		
	def check(self, type, value = 0):
		curtok = self.cur()
		return urtok.type == type if value == 0 else curtok.type == type and curtok.value == value
		
	def cur(self, n = 0):
		return self.tokens[self.tokptr+n] if self.tokptr+n < len(self.tokens) else None
	
	def next(self):
		if(self.srcptr < self.tokens):
			self.tokptr+=1;