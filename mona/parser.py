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
			ast = self.assnExpr()
			
			if(ast != None):
				self.program.append(ast)
				continue
		print(self.program)
	
	def literalExpr(self):
		if( self.check(token.TOKEN_NONALPHA, [token.TOKEN_NUMBER, token.TOKEN_FLOAT, token.TOKEN_STRING, token.TOKEN_BOOLEAN]) ):
			tok = ast.LiteralAST(self.convertTokType(), self.cur().value)
			self.next()
			return tok
		elif( self.check(token.TOKEN_IDENTIFIER) ):
			tok = ast.IdenAST(self.cur().value)
			self.next()
			return tok
		elif( self.check(token.TOKEN_NONALPHA, operator.AT) or self.check(token.TOKEN_NONALPHA, operator.DOLLAR) or self.check(token.TOKEN_NONALPHA, operator.COLON) ):
			tok = ast.NullaryAST(self.cur().value)
			self.next()
			return tok
		elif( self.check(token.TOKEN_NONALPHA, operator.POP) ):
			self.next()
			tok = self.assnExpr()
			if not self.check(token.TOKEN_NONALPHA, operator.PCLS):
				args = []
				
				if type(tok) is not ast.IdenAST:
					self.croak( "Error: Function parameters at the line {} cannot be expressions other than identifiers.".format(self.cur().line) )
				
				args.append(tok)
				
				while True:
					val = self.literalExpr()
					
					if val != None:
						args.append( val )
					else:
						break
				
				self.expect(token.TOKEN_NONALPHA, operator.PCLS, "Error: Expected closing parethensis in function definition at the line {}, but got {} instead".format(self.cur().line, self.cur()) )
				self.next()
				body = self.literalExpr()
				if type(body) is not ast.BlockAST:
					self.croak( "Error: Function at the line {} is expected to have a block.".format(self.cur().line) )
					
				tok = ast.LambdaAST(args, body)
					
			else:
				self.next()
				
			return tok
		elif( self.check(token.TOKEN_NONALPHA, operator.SOP) ):
			self.next()
			tok = self.assnExpr()
			self.expect(token.TOKEN_NONALPHA, operator.SCLS, "Error: Expected closing parethensis at the line {}, but got {} instead".format(self.cur().line, self.cur()) )
			self.next()
			return tok
		elif( self.check(token.TOKEN_NONALPHA, operator.CBOP) ):
			self.next()
			exprs = []
			
			while True:
				val = self.assnExpr()
				
				if val != None:
					exprs.append( val )
				else:
					break
			
			tok = ast.BlockAST( exprs )
			
			self.expect(token.TOKEN_NONALPHA, operator.CBCLS, "Error: Expected closing curly braces at the line {}, but got {} instead".format(self.cur().line, self.cur()) )
			self.next()
			return tok
			
	def postunaryExpr(self):
		tok = self.literalExpr()
		if self.check(token.TOKEN_NONALPHA, [operator.INC, operator.DEC]):
			op = self.cur().value
			self.next()
			tok = ast.PostUnaryAST(op, tok)
			
		return tok
		
	def unaryExpr(self):
		tok = None
		if self.check(token.TOKEN_NONALPHA, [operator.TILDE, operator.NOT, operator.QUES, operator.INC, operator.DEC, operator.BAND, operator.BOR, operator.MINUS, operator.TYPEOF]):
			op = self.cur().value
			self.next()
			tok = ast.PreUnaryAST(op, self.unaryExpr() )
		elif self.check(token.TOKEN_NONALPHA, [operator.AT, operator.DOLLAR, operator.COLON]):
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
		if self.check(token.TOKEN_NONALPHA, [operator.STAR, operator.DIV, operator.MOD, operator.BAND]):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST(op, tok, self.mulExpr() )
			
		return tok
		
	def addExpr(self):
		tok = self.mulExpr()
		if self.check(token.TOKEN_NONALPHA, [operator.PLUS, operator.MINUS, operator.BOR, operator.XOR]):
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
		if self.check(token.TOKEN_NONALPHA, [operator.GRE, operator.GREQ, operator.LE, operator.LEQ, operator.EQ, operator.NOT, operator.ISTYPE]):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST(op, tok, self.logExpr() )
			
		return tok
		
	def condExpr(self):
		tok = self.logExpr()
		cond = None
		res = None
		els = None
		if self.check(token.TOKEN_NONALPHA, [operator.LOOP, operator.TILDE]):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST( op, tok, self.condExpr() )
		elif self.check(token.TOKEN_NONALPHA, operator.QUES):
			op = self.cur().value
			self.next()
			cond = tok
			res = self.condExpr()
			
			if res == None:
				self.croak("Error: Incomplete conditional expression at the line {}.", self.cur().line);
			
			if self.check(token.TOKEN_NONALPHA, operator.COLON):
				self.next()
				els = self.condExpr()
				
				if els == None:
					self.croak("Error: Incomplete conditional expression at the line {}.", self.cur().line);
				
				tok = ast.TernaryAST(op, cond, res, els)
			else:
				tok = ast.BinaryAST(op, cond, res)
		
		return tok
		
	def assnExpr(self):
		tok = self.condExpr()
		if self.check(token.TOKEN_NONALPHA, operator.ASSIGN):
			op = self.cur().value
			self.next()
			tok = ast.BinaryAST( op, tok, self.assnExpr() )
			
		return tok

	def convertTokType(self):
		if self.cur().type == token.TOKEN_NUMBER or self.check(token.TOKEN_KEYWORD, keyword.INTEGER):
			return self.types.getType("Integer")
		if self.cur().type == token.TOKEN_STRING or self.check(token.TOKEN_KEYWORD, keyword.STRING):
			return self.types.getType("String")
		if self.cur().type == token.TOKEN_BOOLEAN or self.check(token.TOKEN_KEYWORD, keyword.BOOLEAN):
			return self.types.getType("Boolean")
		if self.cur().type == token.TOKEN_FLOAT or self.check(token.TOKEN_KEYWORD, keyword.FLOAT):
			return self.types.getType("Float")
	
	def expr(self):
		return self.addExpr
	
	def croak(self,errorMessage):
		print(errorMessage, file=sys.stderr);
		sys.exit()
	
	def expect(self, t, value = 0, onfail = ""):
		curtok = self.cur()
		if type(value) is list:
			if not (curtok.value in value):
				self.croak(onfail)
		else:
			if curtok == None or not (curtok.type == t if value == 0 else curtok.type == t and curtok.value == value):
				self.croak(onfail)
		
	def check(self, t, value = None):
		curtok = self.cur()
		if curtok == None:
			return False
		if type(value) is list:
			return curtok.value in value
		else:
			return curtok.type == t if value == None else (curtok.type == t and curtok.value == value)
		
	def cur(self, n = 0):
		return self.tokens[self.tokptr+n] if self.tokptr+n < len(self.tokens) else None
	
	def next(self):
		if(self.tokptr < len(self.tokens)):
			self.tokptr+=1;