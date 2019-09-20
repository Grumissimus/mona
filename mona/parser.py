import mona.token as token
import mona.operator as operator
import mona.keyword as keyword
import mona.ast as ast
import mona.types as types
import mona.symbol as symbol

import sys

class Parser():
	def __init__(self, token):
		self.tokens = token
		self.tokptr = 0
		self.program = []
		self.types = types.constructDefaultGraph()
		
	def run():
		while( self.cur() != None ):
			continue
		
	def croak(self,errorMessage):
		print(errorMessage, file=sys.stderr);
		sys.exit()
	
	def expect(self, type, value = 0):
		curtok = self.cur()
		return self.curtok.type == type if value == 0 else self.curtok.type == type and self.curtok.value == value
		
	def cur(self, n = 0):
		return self.tokens[self.tokptr+n] if self.tokptr+n < len(self.tokens) else None
	
	def next(self):
		if(self.srcptr < self.tokens):
			self.tokptr+=1;