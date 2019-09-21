import mona.token as token
import mona.operator as operator
import mona.keyword as keyword
import mona.ast as ast
import mona.types as types
import mona.symbol as symbol

import sys

class Parser():
	def __init__(self, tok):
		self.tokens = tok
		self.tokptr = 0
		self.program = []
		self.types = types.constructDefaultGraph()
		self.symtab = symbol.SymbolTable()
		
	def run(self):
		while( self.cur() != None ):
			ast = self.addExpr()
			
			if(ast != None):
				self.program.append(ast)
			
			continue
		print(self.program)
	
	def literalExpr(self):
		if( self.cur().type in [token.TOKEN_NUMBER, token.TOKEN_FLOAT, token.TOKEN_STRING, token.TOKEN_BOOLEAN] ):
			tok = ast.LiteralAST(self.convertTokType(), self.cur().value)
			self.next()
			return tok
		elif( self.check(token.TOKEN_IDENTIFIER) ):
			tok = ast.IdenAST(self.cur().value)
			self.next()
			return tok
		elif( self.check(token.TOKEN_NONALPHA, POP) ):
			self.next()
			tok = self.addExpr()
			self.expect(token.TOKEN_NONALPHA, PCLS)
			return tok
	
	def addExpr(self):
		tok = self.literalExpr()
		if( self.check(token.TOKEN_NONALPHA, operator.PLUS) or self.check(token.TOKEN_NONALPHA, operator.MINUS) ):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST(op, tok, self.addExpr() )
			
		return tok
	
	def convertTokType(self):
		if( self.cur().type == token.TOKEN_NUMBER ):
			return self.types.getType("Integer")
		if( self.cur().type == token.TOKEN_STRING ):
			return self.types.getType("String")
		if( self.cur().type == token.TOKEN_BOOLEAN ):
			return self.types.getType("Boolean")
		if( self.cur().type == token.TOKEN_Float ):
			return self.types.getType("Float")
	
	def expr(self):
		return self.addExpr
	
	def croak(self,errorMessage):
		print(errorMessage, file=sys.stderr);
		sys.exit()
	
	def expect(self, type, value = 0, onfail = ""):
		curtok = self.cur()
		if curtok == None or not curtok.type == type if value == 0 else curtok.type == type and curtok.value == value:
			self.croak(onfail)
		
	def check(self, type, value = 0):
		curtok = self.cur()
		if curtok == None:
			return False
		return curtok.type == type if value == 0 else curtok.type == type and curtok.value == value
		
	def cur(self, n = 0):
		return self.tokens[self.tokptr+n] if self.tokptr+n < len(self.tokens) else None
	
	def next(self):
		if(self.tokptr < len(self.tokens)):
			self.tokptr+=1;