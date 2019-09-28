#abstract base class
class AST(object):
	pass

#integers, floats, strings, types
class LiteralAST(AST):
	def __init__(self, t, v, l = None):
		self.type = t
		self.value = v
		self.lines = l
		
#identifiers
class IdenAST(AST):
	def __init__(self, id, type = None):
		self.id = id
		self.type = type

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
		self.op = op
		self.arg1 = a
		self.arg2 = b

#ternary operators
class TernaryAST(AST):
	def __init__(self, op, a, b, c):
		self.op = op
		self.arg1 = a
		self.arg2 = b
		self.arg3 = c

class FunCallAST(AST):
	def __init__(self, name, args = []):
		self.name = name
		self.args = args
		
#lambda		
class LambdaAST(AST):
	def __init__(self, args, body):
		self.args = args
		self.body = body
		
#blocks		
class BlockAST(AST):
	def __init__(self, b):
		self.block = b