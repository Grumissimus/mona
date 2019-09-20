#abstract base class
class AST(object):
	pass

#identifiers, integers, floats, strings, types
class LiteralAST(AST):
	def __init__(self, t, v):
		self.type = t
		self.value = t

#array literals
class ArrayAST(AST):
	def __init__(self, t, arr):
		self.type = t
		self.value = arr

#operators that require no arguments or operators themselves
class NullaryAST(AST):
	def __init__(self, t):
		self.value = t

#unary operators that require one argument for the left side
class PreUnaryAST(AST):
	def __init__(self, op, t):
		self.op = op
		self.value = t

#unary operators that require one argument for the right side
class PostUnaryAST(AST):
	def __init__(self, op, t):
		self.op = op
		self.value = t

#binary operators
class BinaryAST(AST):
	def __init__(self, op, a, b):
		self.op
		self.arg1 = a
		self.arg2 = b

#ternary operators
class TernaryAST(AST):
	def __init__(self, op, a, b, c):
		self.op
		self.arg1 = a
		self.arg2 = b
		self.arg2 = c

#blocks		
class BlockAST(AST):
	def __init__(self, b):
		self.block = b