import mona.types as type

class Symbol(object):
	pass
	
class Scope(object):
	def __init__(self, name, level):
		self.name = name
		self.level = level
	
	def __eq__(self,other):
		return self.name == other.name and self.level == other.level
	
	def __str__(self):
		return "(" + self.name + ", " + (int)(self.level) + ")"

class Variable(Symbol):
	def __init__(self, type, value, scope):
		self.type = type
		self.value = value
		self.scope = scope
		
	def __str__(self):
		return (str)(value)+" :: "+self.type.name
		
class FunctionArgument:
	def __init__(self, type, name):
		self.name = name
		self.type = type
	
	def __str__(self):
		return self.type.name+" "+self.name
		
class Function(Symbol):
	def __init__(self, type, argNum, param, body, retType, scope):
		self.type = type
		self.argNum = argNum
		self.param = param
		self.body = body
		self.retType = retType
		self.scope = scope
		
	def __str__(self):
		return "("+self.type.name+","+(str)(value)+")"
		
class DataType(Symbol):
	def __init__(self, type):
		self.type = type

class SymbolTable:
	def __init__(self):
		self.table = {}
	
	def getSymbol(self, name):
		try:
			return self.table[name]
		except:
			return None
	
	def insertSymbol(self, name, sym):
		if name in self.table:
			self.table[name].append(sym)
		else:
			self.table[name] = [sym]
			
	def removeSymbol(self, name, scope = None):
		symToDel = self.getSymbol(name)
	
		if(symToDel == None):
			return
		
		if scope != None:
			for i in symToDel:
				if i.scope == scope:
					del i
					return
		else:
			del symToDel