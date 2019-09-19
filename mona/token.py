TOKEN_IDENTIFIER = 0
TOKEN_KEYWORD = 1
TOKEN_NUMBER = 2
TOKEN_STRING = 3
TOKEN_FLOAT = 4
TOKEN_BOOLEAN = 5
TOKEN_NONALPHA = 6

class Token():
	def __init__(self, type, value, line):
		self.type = type
		self.value = value
		self.line = line
		
	def __str__(self):
		return "(" + (str)(self.type) + ", " + (str)(self.value) + ", " + (str)(self.line) + ")"
		