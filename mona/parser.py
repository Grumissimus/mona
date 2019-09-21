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
			ast = self.logExpr()
			
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
		elif( self.check(token.TOKEN_NONALPHA, operator.AT) or self.check(token.TOKEN_NONALPHA, operator.DOLLAR) ):
			tok = ast.NullaryAST(self.cur().value)
			self.next()
			return tok
		elif( self.check(token.TOKEN_NONALPHA, operator.POP) ):
			self.next()
			tok = self.logExpr()
			self.expect(token.TOKEN_NONALPHA, operator.PCLS, "Error: Expected closing parethensis in the line {}, but got {} instead".format(self.cur().line, self.cur()) )
			self.next()
			return tok
			
	def postunaryExpr(self):
		tok = self.literalExpr()
		if( 
			self.check(token.TOKEN_NONALPHA, operator.INC) or 
			self.check(token.TOKEN_NONALPHA, operator.DEC)
		):
			op = self.cur().value
			self.next()
			tok = ast.PostUnaryAST(op, self.postunaryExpr() )
			
		return tok
		
	def unaryExpr(self):
		tok = None
		if( self.check(token.TOKEN_NONALPHA, operator.TILDE) or 
			self.check(token.TOKEN_NONALPHA, operator.NOT) or 
			self.check(token.TOKEN_NONALPHA, operator.QUES) or 
			self.check(token.TOKEN_NONALPHA, operator.INC) or 
			self.check(token.TOKEN_NONALPHA, operator.DEC) or 
			self.check(token.TOKEN_NONALPHA, operator.BAND) or 
			self.check(token.TOKEN_NONALPHA, operator.BOR) or 
			self.check(token.TOKEN_NONALPHA, operator.MINUS) or 
			self.check(token.TOKEN_NONALPHA, operator.TYPEOF)
		):
			op = self.cur().value
			self.next()
			tok = ast.PreUnaryAST(op, self.unaryExpr() )
		elif self.check(token.TOKEN_NONALPHA, operator.AT) or self.check(token.TOKEN_NONALPHA, operator.DOLLAR):
			prev = self.tokptr
			op = self.cur().value
			self.next()
			arg = self.unaryExpr()
			if arg != None:
				tok = ast.PreUnaryAST(op, arg)
				return tok
			self.tokptr = prev
			
		return tok if tok != None else self.postunaryExpr()
	
	def powExpr(self):
		tok = self.unaryExpr()
		if( self.check(token.TOKEN_NONALPHA, operator.POWER) ):
			op = self.cur().value
			self.next()
			tok = ast.PreUnaryAST(op, tok, self.powExpr() )
			
		return tok
		
	def mulExpr(self):
		tok = self.powExpr()
		if( self.check(token.TOKEN_NONALPHA, operator.STAR) 
			or self.check(token.TOKEN_NONALPHA, operator.DIV) 
			or self.check(token.TOKEN_NONALPHA, operator.MOD) 
			or self.check(token.TOKEN_NONALPHA, operator.BAND) 
		):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST(op, tok, self.mulExpr() )
			
		return tok
		
	def addExpr(self):
		tok = self.mulExpr()
		if( self.check(token.TOKEN_NONALPHA, operator.PLUS) 
			or self.check(token.TOKEN_NONALPHA, operator.MINUS) 
			or self.check(token.TOKEN_NONALPHA, operator.BOR) 
			or self.check(token.TOKEN_NONALPHA, operator.XOR) 
		):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST(op, tok, self.addExpr() )
			
		return tok
	
	def shfExpr(self):
		tok = self.addExpr()
		if( self.check(token.TOKEN_NONALPHA, operator.SHR) 
			or self.check(token.TOKEN_NONALPHA, operator.SHL) 
		):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST(op, tok, self.shfExpr() )
			
		return tok
		
	def logExpr(self):
		tok = self.shfExpr()
		if( self.check(token.TOKEN_NONALPHA, operator.GRE) 
			or self.check(token.TOKEN_NONALPHA, operator.GREQ) 
			or self.check(token.TOKEN_NONALPHA, operator.LE) 
			or self.check(token.TOKEN_NONALPHA, operator.LE) 
			or self.check(token.TOKEN_NONALPHA, operator.EQ) 
			or self.check(token.TOKEN_NONALPHA, operator.NOT) 
			or self.check(token.TOKEN_NONALPHA, operator.ISTYPE) 
		):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST(op, tok, self.logExpr() )
			
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
		if curtok == None or not (curtok.type == type if value == 0 else curtok.type == type and curtok.value == value):
			self.croak(onfail)
		
	def check(self, type, value = None):
		curtok = self.cur()
		if curtok == None:
			return False
		return curtok.type == type if value == None else (curtok.type == type and curtok.value == value)
		
	def cur(self, n = 0):
		return self.tokens[self.tokptr+n] if self.tokptr+n < len(self.tokens) else None
	
	def next(self):
		if(self.tokptr < len(self.tokens)):
			self.tokptr+=1;